"""Efeitos sonoros automáticos de um episódio: papel batendo, fita, carimbo, tesoura e virada de página
nos tempos de entrada de cada elemento do index.html.

Uso:  python ferramentas/gerar_efeitos.py episodios/<serie>/<EP>      → grava <EP>/sfx.wav
"""
import re, os, sys, numpy as np, soundfile as sf
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = sys.argv[1]
SR = 48000; D = os.path.join(KIT, 'biblioteca', 'efeitos-sonoros') + os.sep
DUR = float(re.search(r"DUR = ([\d.]+)", open(os.path.join(EP, 'index.html'), encoding='utf-8').read()).group(1))
FOL = {k: (lambda x: x if x.ndim == 1 else x.mean(1))(sf.read(D + k + '.wav')[0]) for k in ('pages', 'tape', 'scissors', 'crumple')}
def seg(name, t0, dur, fade=0.05):
    x = FOL[name]; a = max(0, int((t0 - 0.012) * SR)); s = x[a:a + int((dur + 0.012) * SR)].copy()
    s[:96] *= np.linspace(0, 1, 96); f = int(fade * SR); s[-f:] *= np.linspace(1, 0, f) ** 2
    return s / (np.abs(s).max() + 1e-9)
PAGE = [13.84, 25.97, 23.28, 4.39, 5.78, 17.76, 26.13]; TAPE = [0.37, 2.99, 9.09, 6.13]; SNIP = [1.02, 1.74, 3.11, 4.76]
def thud():
    t = np.arange(int(0.12 * SR)) / SR; return np.sin(2 * np.pi * (90 - 300 * t) * t) * np.exp(-t * 35)
def stamp():
    t = np.arange(int(0.09 * SR)) / SR; rng = np.random.default_rng(3); return (rng.standard_normal(len(t)) * 0.5 + np.sin(2 * np.pi * 140 * t)) * np.exp(-t * 60)
L = int(DUR * SR); out = np.zeros((L, 2))
def add(s, t, g=0, pan=0):
    i = int(t * SR)
    if i >= L: return
    s = s[:L - i] * 10 ** (g / 20); out[i:i + len(s), 0] += s * (1 - pan); out[i:i + len(s), 1] += s * (1 + pan)
html = open(os.path.join(EP, 'index.html'), encoding='utf-8').read()
k = 0
for line in html.splitlines():
    m = re.search(r"k: '(\w+)'.*?in: ([\d.]+)", line)
    if not m or 'E({' not in line: continue
    kind, t = m.group(1), float(m.group(2)); k += 1; pan = ((k * 37) % 9 - 4) / 12
    anim = re.search(r"anim: '(\w+)'", line); anim = anim.group(1) if anim else 'slap'
    if anim == 'none': continue
    if "per: 'letter'" in line:
        txt = re.search(r"text: '([^']*)'", line).group(1).replace('\\n', '').replace(' ', '')
        for j in range(min(len(txt), 14)): add(seg('pages', PAGE[j % 7], 0.15), t + j / 12, -9, ((j % 3) - 1) * 0.2); add(thud(), t + j / 12, -9)
    elif kind == 'stamp': add(stamp(), t, -6, pan); add(thud(), t, -5, pan)
    elif kind == 'tag': add(seg('tape', TAPE[k % 4], 0.18), t, -11, pan)
    elif kind == 'circle': add(seg('scissors', SNIP[k % 4], 0.3), t, -8, pan)
    elif anim in ('slideR', 'slideL'): add(seg('pages', PAGE[3], 0.25, 0.1), t, -8, pan)
    else: add(seg('pages', PAGE[k % 7], 0.2), t, -5, pan); add(thud(), t, -6, pan)
    s = re.search(r"strike: ([\d.]+)", line)
    if s: add(seg('scissors', SNIP[2], 0.25), float(s.group(1)), -8, pan)
for t in [float(x) for x in re.findall(r"scene\('\w+', ([\d.]+),", html)][1:]: add(seg('pages', PAGE[(int(t) + 3) % 7], 0.34, 0.12), t, -4, 0.4)
sf.write(os.path.join(EP, 'sfx.wav'), out * 0.5, SR)
print('ok', np.abs(out).max())
