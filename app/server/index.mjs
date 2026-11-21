import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import express from 'express';
import multer from 'multer';
import { APP, KIT, PORT, PYTHON, chrome, kitEnv, ffmpegBin } from './config.mjs';
import { statusClaude, abrirLogin, sair, testar, lerConfig, gravarConfig } from './claude.mjs';
import { criarJob, pegarJob, listarJobs, jobAtual, cancelarJob, resumo } from './jobs.mjs';

const app = express();
const tmp = path.join(KIT, 'entrada', '_upload'); // mesmo disco do kit (rename sem cópia)
fs.mkdirSync(tmp, { recursive: true });
const upload = multer({ dest: tmp, limits: { fileSize: 300 * 1024 * 1024 } });

app.use(express.json());

app.get('/api/ping', (_req, res) => res.json({ estudio: 'cafe-contado' })); // resposta imediata (usada pelo .bat)

app.get('/api/saude', async (_req, res) => {
  const roda = (cmd, args) => { try { return spawnSync(cmd, args, { env: kitEnv(), timeout: 8000 }).status === 0; } catch { return false; } };
  res.json({
    kit: fs.existsSync(path.join(KIT, 'CAFE-CONTADO.md')) ? KIT : null,
    ffmpeg: roda(ffmpegBin(), ['-version']) && roda(ffmpegBin('ffprobe'), ['-version']),
    python: roda(PYTHON, ['--version']),
    chrome: Boolean(chrome()),
    claude: await statusClaude().catch(() => ({ pronto: false })),
    atual: jobAtual() ? resumo(jobAtual()) : null,
  });
});

app.get('/api/jobs', (_req, res) => res.json(listarJobs()));

app.post('/api/jobs', upload.fields([{ name: 'narracao', maxCount: 1 }, { name: 'musica', maxCount: 1 }]), async (req, res) => {
  const limpar = () => Object.values(req.files || {}).flat().forEach((f) => fs.rmSync(f.path, { force: true }));
  try {
    const { titulo = '', selo = '', copy = '', prompt = '', renderizar = '1' } = req.body;
    const narracao = req.files?.narracao?.[0];
    const musica = req.files?.musica?.[0];
    const falta = [!titulo.trim() && 'título', !selo.trim() && 'selo', !copy.trim() && 'copy', !narracao && 'narração', !musica && 'música'].filter(Boolean);
    if (falta.length) { limpar(); return res.status(400).json({ erro: `Falta: ${falta.join(', ')}.` }); }
    const j = await criarJob({ titulo: titulo.trim(), selo: selo.trim(), copy, prompt, renderizar: renderizar !== '0', narracao, musica });
    res.json(resumo(j));
  } catch (e) {
    limpar();
    res.status(409).json({ erro: String(e.message || e) });
  }
});

app.get('/api/jobs/:id', (req, res) => {
  const j = pegarJob(req.params.id);
  j ? res.json({ ...resumo(j), eventos: j.eventos }) : res.status(404).json({ erro: 'não encontrado' });
});

// Eventos ao vivo (SSE): reenvia o histórico e segue transmitindo
app.get('/api/jobs/:id/eventos', (req, res) => {
  const j = pegarJob(req.params.id);
  if (!j) return res.status(404).end();
  res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
  const enviar = (ev) => res.write(`data: ${JSON.stringify(ev)}\n\n`);
  j.eventos.forEach(enviar);
  j.on('evento', enviar);
  const ping = setInterval(() => res.write(': ping\n\n'), 20000);
  req.on('close', () => { clearInterval(ping); j.off('evento', enviar); });
});

app.post('/api/jobs/:id/cancelar', (req, res) => {
  const j = pegarJob(req.params.id);
  if (!j) return res.status(404).end();
  cancelarJob(j);
  res.json({ ok: true });
});

// Imagens do episódio (prévia e capa)
app.get('/api/jobs/:id/imagem/:nome', (req, res) => {
  const j = pegarJob(req.params.id);
  const nome = { contato: 'contato.jpg', capa: 'capa.jpg' }[req.params.nome];
  if (!j || !nome) return res.status(404).end();
  const f = path.join(KIT, 'episodios', 'cafe-contado', j.ep, 'out', nome);
  fs.existsSync(f) ? res.set('Cache-Control', 'no-store').sendFile(f) : res.status(404).end();
});

app.post('/api/jobs/:id/abrir-pasta', (req, res) => {
  const j = pegarJob(req.params.id);
  if (!j?.pasta) return res.status(404).end();
  const p = path.join(KIT, j.pasta);
  if (process.platform === 'win32') spawnSync('explorer.exe', [p]);
  res.json({ ok: true, pasta: p });
});

// Configuração e login do Claude
const tentar = (fn) => async (req, res) => {
  try { res.json(await fn(req)); } catch (e) { res.status(400).json({ erro: String(e.message || e) }); }
};
app.get('/api/claude/status', tentar(() => statusClaude()));
app.post('/api/claude/login', tentar((req) => { abrirLogin(req.body?.modo); return { ok: true }; }));
app.post('/api/claude/sair', tentar(async () => { await sair(); return statusClaude(); }));
app.post('/api/claude/testar', tentar(() => testar()));
app.get('/api/config', tentar(() => lerConfig()));
app.put('/api/config', tentar((req) => gravarConfig(req.body || {})));

// Fontes do kit para a interface
app.use('/fontes', express.static(path.join(KIT, 'biblioteca', 'fontes')));

// Produção: serve o build do React
const dist = path.join(APP, 'dist');
if (fs.existsSync(dist)) {
  app.use(express.static(dist));
  app.get(/^\/(?!api\/).*/, (_req, res) => res.sendFile(path.join(dist, 'index.html')));
}

// Express 5 entrega o erro de porta no callback (sem lançar): tratar aqui, senão o processo sai calado
app.listen(PORT, (err) => {
  if (err) {
    if (err.code === 'EADDRINUSE') {
      console.error(`\nERRO: a porta ${PORT} já está em uso.`);
      console.error('Provavelmente o estúdio já está aberto em outra janela: use http://localhost:' + PORT);
      console.error('Se não estiver, feche o programa que usa essa porta ou defina PORT=outra no app/.env.');
    } else {
      console.error('\nERRO ao iniciar o servidor:', err.message || err);
    }
    process.exit(1);
  }
  console.log(`Café Contado · app em http://localhost:${PORT}`);
  console.log(`kit: ${KIT}`);
});

process.on('uncaughtException', (e) => console.error('ERRO inesperado:', e?.stack || e));
process.on('unhandledRejection', (e) => console.error('ERRO inesperado:', e?.stack || e));
