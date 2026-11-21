import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
export const APP = path.resolve(here, '..');
const ENV_FILE = path.join(APP, '.env');

// ---------------------------------------------------------------- .env simples (CHAVE=valor por linha)
function lerEnvArquivo() {
  const out = {};
  if (!fs.existsSync(ENV_FILE)) return out;
  for (const ln of fs.readFileSync(ENV_FILE, 'utf8').split(/\r?\n/)) {
    const m = ln.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (m) out[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  return out;
}
for (const [k, v] of Object.entries(lerEnvArquivo())) if (!(k in process.env)) process.env[k] = v;

/** Grava/atualiza chaves no .env (valor vazio remove) e aplica no processo na hora. */
export function salvarEnv(patch) {
  const atual = lerEnvArquivo();
  for (const [k, v] of Object.entries(patch)) {
    if (v === undefined) continue;
    if (v === '' || v === null) { delete atual[k]; delete process.env[k]; }
    else { atual[k] = String(v); process.env[k] = String(v); }
  }
  const txt = Object.entries(atual).map(([k, v]) => `${k}=${v}`).join('\n') + '\n';
  fs.writeFileSync(ENV_FILE, txt, 'utf8');
}

// ---------------------------------------------------------------- configurações (lidas na hora, editáveis pela tela)
export const KIT = path.resolve(APP, process.env.KIT_DIR || '../kit-cafe-contado');
export const PORT = Number(process.env.PORT || 3001);
export const PYTHON = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');

export const MODELOS = ['claude-opus-5-5', 'claude-sonnet-5-5', 'claude-fable-5-2'];
export const ESFORCOS = ['low', 'medium', 'high', 'xhigh', 'max'];

export function cfg() {
  return {
    modelo: process.env.ESTUDIO_MODELO || 'claude-opus-5-5',
    esforco: process.env.ESTUDIO_ESFORCO || 'high',
    workers: Number(process.env.ESTUDIO_WORKERS || 6),
    apiKey: process.env.ANTHROPIC_API_KEY || '',
  };
}

const TOOLS = path.join(KIT, 'motor', 'tools');

export function chrome() {
  if (process.env.MG_CHROME) return process.env.MG_CHROME;
  const c = [
    path.join(process.env.ProgramFiles || '', 'Google/Chrome/Application/chrome.exe'),
    path.join(process.env['ProgramFiles(x86)'] || '', 'Google/Chrome/Application/chrome.exe'),
    path.join(process.env.LOCALAPPDATA || '', 'Google/Chrome/Application/chrome.exe'),
    path.join(process.env['ProgramFiles(x86)'] || '', 'Microsoft/Edge/Application/msedge.exe'),
  ];
  return c.find((p) => p && fs.existsSync(p)) || '';
}

/** Executável do Claude Code (para login/status). */
export function claudeBin() {
  const exe = process.platform === 'win32' ? 'claude.exe' : 'claude';
  const casa = process.env.USERPROFILE || process.env.HOME || '';
  const cands = [process.env.CLAUDE_BIN, path.join(casa, '.local', 'bin', exe),
    ...(process.env.PATH || process.env.Path || '').split(path.delimiter).map((d) => path.join(d, exe))];
  return cands.find((p) => p && fs.existsSync(p)) || null;
}

/** Ambiente dos processos do kit: ffmpeg do motor/tools no PATH, Python em UTF-8, Chrome do motor. */
export function kitEnv() {
  const env = { ...process.env };
  const key = Object.keys(env).find((k) => k.toLowerCase() === 'path') || 'PATH';
  env[key] = TOOLS + path.delimiter + (env[key] || '');
  env.PYTHONUTF8 = '1';
  env.PYTHONIOENCODING = 'utf-8';
  const ch = chrome();
  if (ch) env.MG_CHROME = ch;
  return env;
}

export function ffmpegBin(nome = 'ffmpeg') {
  const local = path.join(TOOLS, nome + (process.platform === 'win32' ? '.exe' : ''));
  return fs.existsSync(local) ? local : nome;
}
