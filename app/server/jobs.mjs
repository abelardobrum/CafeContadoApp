import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { EventEmitter } from 'node:events';
import { query } from '@anthropic-ai/claude-agent-sdk';
import { KIT, cfg, kitEnv, ffmpegBin } from './config.mjs';
import { SISTEMA, montarPedido } from './prompt.mjs';

const jobs = new Map();
let atual = null; // um episódio por vez (render é pesado)

export const jobAtual = () => atual;
export const pegarJob = (id) => jobs.get(id);
export const listarJobs = () => [...jobs.values()].map(resumo).reverse();

export function resumo(j) {
  const { id, ep, slug, titulo, selo, fase, status, erro, pasta, progresso, custo, criado, renderizar } = j;
  return { id, ep, slug, titulo, selo, fase, status, erro, pasta, progresso, custo, criado, renderizar };
}

export function slugify(t) {
  return t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48).replace(/-+$/, '') || 'episodio';
}

function slugLivre(base) {
  let s = base, n = 2;
  const ocupado = (x) => fs.existsSync(path.join(KIT, 'entrada', x)) ||
    fs.existsSync(path.join(KIT, 'episodios', 'cafe-contado', x.toUpperCase()));
  while (ocupado(s)) s = `${base}-${n++}`;
  return s;
}

/** Cria o job: grava os arquivos em entrada/<slug>/ (mp3) e dispara o fluxo. */
export async function criarJob({ titulo, selo, copy, prompt, renderizar, narracao, musica }) {
  if (atual) throw new Error(`Já há um episódio em produção (${atual.ep}). Aguarde terminar ou cancele.`);
  const slug = slugLivre(slugify(titulo));
  const ep = slug.toUpperCase();
  const dir = path.join(KIT, 'entrada', slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'copy.txt'), copy.trim() + '\n', 'utf8');
  await paraMp3(narracao, path.join(dir, 'narr.mp3'));
  await paraMp3(musica, path.join(dir, 'musica.mp3'));
  fs.writeFileSync(path.join(dir, 'pedido.json'), JSON.stringify({ titulo, selo, prompt, renderizar, criado: new Date().toISOString() }, null, 2), 'utf8');

  const j = Object.assign(new EventEmitter(), {
    id: slug, ep, slug, titulo, selo, prompt, renderizar,
    fase: 'claude', status: 'rodando', erro: null, pasta: null, progresso: null, custo: null,
    criado: Date.now(), eventos: [], abort: new AbortController(), filho: null,
  });
  j.setMaxListeners(50);
  jobs.set(j.id, j);
  atual = j;
  rodar(j).catch((e) => falhar(j, e)).finally(() => { if (atual === j) atual = null; });
  return j;
}

export function cancelarJob(j) {
  j.cancelado = true;
  j.abort.abort();
  if (j.filho) j.filho.kill();
}

// ------------------------------------------------------------------ eventos
const logDe = (j) => path.join(KIT, 'entrada', j.slug, 'log.txt');

function emitir(j, ev) {
  ev.t = Date.now();
  j.eventos.push(ev);
  j.emit('evento', ev);
  try {
    const linha = ev.tipo === 'estado' ? `[${ev.fase}] ${ev.status}` : `${ev.tipo}: ${ev.texto ?? ''}`;
    fs.appendFileSync(logDe(j), linha + '\n', 'utf8');
  } catch { /* log é opcional */ }
}

function estado(j, patch) {
  Object.assign(j, patch);
  emitir(j, { tipo: 'estado', ...resumo(j) });
}

function falhar(j, e) {
  estado(j, { status: j.cancelado ? 'cancelado' : 'erro', erro: j.cancelado ? 'Cancelado pelo usuário.' : String(e?.message || e) });
}

// ------------------------------------------------------------------ fluxo
async function rodar(j) {
  emitir(j, { tipo: 'info', texto: `Arquivos salvos em entrada/${j.slug}/ · EP ${j.ep}` });
  estado(j, { fase: 'claude' });
  await rodarClaude(j);

  const epDir = path.join(KIT, 'episodios', 'cafe-contado', j.ep);
  const destTxt = path.join(epDir, 'destino.txt');
  if (!fs.existsSync(destTxt)) throw new Error('O Claude terminou sem rodar o "cc.py finalizar" (não há destino.txt). Veja o log.');
  const destino = path.resolve(KIT, fs.readFileSync(destTxt, 'utf8').trim().replace(/\\/g, '/'));
  estado(j, { pasta: path.relative(KIT, destino) });

  if (!j.renderizar) {
    emitir(j, { tipo: 'info', texto: `Render pulado. Para renderizar depois: 2 cliques em episodios\\cafe-contado\\${j.ep}\\RENDER.bat` });
    estado(j, { fase: 'pronto', status: 'ok' });
    return;
  }
  estado(j, { fase: 'render', progresso: 0 });
  await renderizar(j, epDir, destino);
  estado(j, { fase: 'pronto', status: 'ok', progresso: 1 });
}

function resumoFerramenta(nome, inp = {}) {
  if (nome === 'Bash') return inp.command;
  if (inp.file_path) return path.relative(KIT, inp.file_path) || inp.file_path;
  if (inp.pattern) return inp.pattern;
  return JSON.stringify(inp).slice(0, 200);
}

async function rodarClaude(j) {
  const { modelo, esforco } = cfg();
  emitir(j, { tipo: 'info', texto: `Claude: ${modelo} · esforço ${esforco}` });
  const q = query({
    prompt: montarPedido(j),
    options: {
      cwd: KIT,
      model: modelo,
      effort: esforco,
      env: kitEnv(),
      abortController: j.abort,
      systemPrompt: { type: 'preset', preset: 'claude_code', append: SISTEMA },
      allowedTools: ['Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash'],
      disallowedTools: ['WebSearch', 'WebFetch', 'Agent', 'Task'],
      permissionMode: 'acceptEdits',
      maxTurns: 80,
    },
  });

  let final = null;
  for await (const m of q) {
    if (m.type === 'assistant' && !m.parent_tool_use_id) {
      if (m.error) emitir(j, { tipo: 'erro', texto: `Claude: ${m.error}` });
      for (const b of m.message?.content || []) {
        if (b.type === 'text' && b.text.trim()) emitir(j, { tipo: 'claude', texto: b.text.trim() });
        if (b.type === 'tool_use') {
          emitir(j, { tipo: 'ferramenta', nome: b.name, texto: resumoFerramenta(b.name, b.input) });
          if (b.name === 'Read' && /contato\.jpg$/.test(b.input?.file_path || '')) emitir(j, { tipo: 'previa' });
        }
      }
    } else if (m.type === 'user' && !m.parent_tool_use_id) {
      const c = m.message?.content;
      for (const b of Array.isArray(c) ? c : []) {
        if (b.type !== 'tool_result') continue;
        const txt = (Array.isArray(b.content) ? b.content.filter((x) => x.type === 'text').map((x) => x.text).join('\n') : String(b.content ?? '')).trim();
        if (txt) emitir(j, { tipo: b.is_error ? 'erro' : 'saida', texto: txt.length > 1500 ? txt.slice(0, 1500) + '\n…' : txt });
      }
    } else if (m.type === 'result') {
      final = m;
    }
  }
  if (!final) throw new Error('A sessão do Claude terminou sem resultado.');
  estado(j, { custo: final.total_cost_usd ?? null });
  if (final.subtype !== 'success' || final.is_error) {
    throw new Error(`Claude parou (${final.subtype}${final.result ? ': ' + final.result : ''})`);
  }
}

// ------------------------------------------------------------------ render
function renderizar(j, epDir, destino) {
  const WORKERS = cfg().workers;
  return new Promise((ok, falha) => {
    const saida = path.join(KIT, 'saida');
    fs.mkdirSync(saida, { recursive: true });
    const mp4 = path.join(saida, `${j.ep}.mp4`);
    const args = [path.join(KIT, 'motor', 'render.mjs'), path.relative(KIT, epDir),
      '--audio', path.join(path.relative(KIT, epDir), 'audio.flac'), '--out', path.relative(KIT, mp4), '--workers', String(WORKERS)];
    emitir(j, { tipo: 'info', texto: `Renderizando (${WORKERS} processos, ~8 min)…` });
    const p = spawn(process.execPath, args, { cwd: KIT, env: kitEnv() });
    j.filho = p;
    const linhas = (buf) => {
      for (const ln of buf.toString().split(/\r?\n/)) {
        if (!ln.trim()) continue;
        const m = ln.match(/(\d+)\/(\d+) frames/);
        if (m) { j.progresso = Number(m[1]) / Number(m[2]); emitir(j, { tipo: 'progresso', valor: j.progresso, texto: ln.trim() }); }
        else emitir(j, { tipo: 'render', texto: ln.trim() });
      }
    };
    p.stdout.on('data', linhas);
    p.stderr.on('data', linhas);
    p.on('error', falha);
    p.on('close', (code) => {
      j.filho = null;
      if (j.cancelado) return falha(new Error('cancelado'));
      if (code !== 0 || !fs.existsSync(mp4)) return falha(new Error(`Render falhou (código ${code}). Veja o log.`));
      const final = path.join(destino, path.basename(destino) + '.mp4');
      fs.mkdirSync(destino, { recursive: true });
      fs.copyFileSync(mp4, final);
      emitir(j, { tipo: 'info', texto: `Vídeo pronto: ${path.relative(KIT, final)}` });
      ok();
    });
  });
}

// ------------------------------------------------------------------ áudio
function paraMp3(arq, destino) {
  const ext = path.extname(arq.originalname || '').toLowerCase();
  if (ext === '.mp3') { fs.renameSync(arq.path, destino); return Promise.resolve(); }
  return new Promise((ok, falha) => {
    const p = spawn(ffmpegBin(), ['-v', 'error', '-y', '-i', arq.path, '-vn', '-codec:a', 'libmp3lame', '-q:a', '2', destino]);
    let err = '';
    p.stderr.on('data', (d) => (err += d));
    p.on('error', falha);
    p.on('close', (c) => {
      fs.rmSync(arq.path, { force: true });
      c === 0 ? ok() : falha(new Error(`Não consegui converter ${arq.originalname} para mp3: ${err.trim()}`));
    });
  });
}
