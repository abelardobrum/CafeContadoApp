import { spawn, execFile } from 'node:child_process';
import { query } from '@anthropic-ai/claude-agent-sdk';
import { APP, cfg, salvarEnv, claudeBin, MODELOS, ESFORCOS } from './config.mjs';

const mascarar = (k) => (k ? `${k.slice(0, 10)}…${k.slice(-4)}` : '');

function rodarClaude(args, timeout = 15000) {
  const bin = claudeBin();
  if (!bin) return Promise.resolve({ ok: false, saida: '', erro: 'Claude Code não encontrado nesta máquina.' });
  return new Promise((res) => {
    execFile(bin, args, { timeout, windowsHide: true }, (err, stdout, stderr) =>
      res({ ok: !err, saida: stdout.trim(), erro: (stderr || err?.message || '').trim() }));
  });
}

/** Situação do login: conta do Claude Code e/ou chave de API do .env (a chave tem prioridade). */
export async function statusClaude() {
  const { apiKey, modelo } = cfg();
  const bin = claudeBin();
  let conta = { loggedIn: false };
  if (bin) {
    const r = await rodarClaude(['auth', 'status', '--json']);
    try { conta = JSON.parse(r.saida); } catch { conta = { loggedIn: false, erro: r.erro || r.saida }; }
  }
  const metodo = apiKey ? 'chave' : conta.loggedIn ? 'conta' : null;
  return {
    pronto: Boolean(metodo),
    metodo,
    modelo,
    cli: Boolean(bin),
    conta: conta.loggedIn ? { email: conta.email, plano: conta.subscriptionType, tipo: conta.authMethod, org: conta.orgName } : null,
    chave: mascarar(apiKey),
  };
}

/** Abre uma janela de terminal com o login do Claude (o navegador abre para autorizar). */
export function abrirLogin(modo = 'claudeai') {
  const bin = claudeBin();
  if (!bin) throw new Error('Claude Code não está instalado. Instale em https://claude.com/claude-code ou use uma chave de API.');
  const flag = modo === 'console' ? '--console' : '--claudeai';
  if (process.platform !== 'win32') {
    spawn(bin, ['auth', 'login', flag], { detached: true, stdio: 'ignore' }).unref();
    return;
  }
  const cmd = `/c start "Login do Claude" cmd /k ""${bin}" auth login ${flag} && echo. && echo Login concluido. Pode fechar esta janela e voltar ao estudio."`;
  spawn('cmd.exe', [cmd], { detached: true, stdio: 'ignore', windowsVerbatimArguments: true, cwd: APP }).unref();
}

export async function sair() {
  const r = await rodarClaude(['auth', 'logout']);
  if (!r.ok) throw new Error(r.erro || 'Falha ao sair');
}

/** Chamada mínima pelo mesmo caminho dos episódios (Agent SDK). */
export async function testar() {
  const { modelo } = cfg();
  const t0 = Date.now();
  let init = null, fim = null;
  for await (const m of query({ prompt: 'Responda apenas: OK', options: { model: modelo, effort: 'low', maxTurns: 1, allowedTools: [], cwd: APP } })) {
    if (m.type === 'system' && m.subtype === 'init') init = m;
    if (m.type === 'assistant' && m.error) throw new Error(`Claude recusou: ${m.error}`);
    if (m.type === 'result') fim = m;
  }
  if (!fim || fim.subtype !== 'success' || fim.is_error) throw new Error(fim?.result || 'Sem resposta do Claude');
  return { resposta: fim.result, modelo: init?.model || modelo, origem: init?.apiKeySource, segundos: (Date.now() - t0) / 1000 };
}

export function lerConfig() {
  const c = cfg();
  return { modelo: c.modelo, esforco: c.esforco, workers: c.workers, chave: mascarar(c.apiKey), modelos: MODELOS, esforcos: ESFORCOS };
}

export function gravarConfig({ modelo, esforco, workers, chave }) {
  const patch = {};
  if (modelo !== undefined) { if (!/^claude-[a-z0-9-]+$/.test(modelo)) throw new Error('Modelo inválido'); patch.ESTUDIO_MODELO = modelo; }
  if (esforco !== undefined) { if (!ESFORCOS.includes(esforco)) throw new Error('Esforço inválido'); patch.ESTUDIO_ESFORCO = esforco; }
  if (workers !== undefined) { const n = Number(workers); if (!(n >= 1 && n <= 32)) throw new Error('Processos: 1 a 32'); patch.ESTUDIO_WORKERS = String(Math.round(n)); }
  if (chave !== undefined) {
    const k = String(chave).trim();
    if (k && !k.startsWith('sk-ant-')) throw new Error('A chave da API começa com sk-ant-');
    patch.ANTHROPIC_API_KEY = k; // vazio = remove
  }
  salvarEnv(patch);
  return lerConfig();
}
