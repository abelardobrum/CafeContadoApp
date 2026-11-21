"""Helpers para desenhar peças novas do Café Contado (MIT). Uso, sem ler mais nada:

    import sys, os; sys.path.insert(0, os.path.join(KIT, 'ferramentas', 'geradores-de-imagens'))
    from pecas import canvas, S, finish, registrar, INK, CREAM
    im, d = canvas(460, 440)                 # desenha com PIL.ImageDraw; envolva coordenadas em S(...)
    d.ellipse(S((40, 60, 400, 360)), fill=(104, 64, 34))
    finish(im, 'nome', 'objetos')            # recorte branco + halftone -> biblioteca/objetos/nome.png
    registrar(['nome'], 'objetos', 'EP')     # grava no indice.json

Tamanho: desenhe ~300–500 px; no cenas.js s 0.6–0.9 já fica grande.
"""
import math, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SS = 2
INK = (28, 24, 20); CREAM = (243, 236, 220)


def canvas(w, h):
    im = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def S(v):
    if isinstance(v, (list, tuple)):
        return [tuple(c * SS for c in x) if isinstance(x, tuple) else x * SS for x in v]
    return v * SS


def tone(im, period=3.6, mix=0.25):
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    lum = (0.3 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]) / 255
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    c, s = math.cos(0.785), math.sin(0.785)
    u = (xx * c - yy * s) / period; v = (xx * s + yy * c) / period
    d = np.hypot(u - np.round(u), v - np.round(v))
    dot = (d < np.sqrt(np.clip(1 - lum, 0, 1)) * 0.55).astype(np.float32)
    rgb = rgb * (1 - mix * dot[..., None] * 0.55)
    return Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), al], -1).astype(np.uint8))


def finish(im, name, categoria='objetos', border=3):
    out = os.path.join(KIT, 'biblioteca', categoria); os.makedirs(out, exist_ok=True)
    im = tone(im.resize((im.width // SS, im.height // SS), Image.LANCZOS), 3.6, 0.45)
    pad = border + 6
    big = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0)); big.paste(im, (pad, pad))
    rim = big.split()[3].point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(border * 2 + 1))
    rim = rim.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else 0)
    white = Image.new('RGBA', big.size, (250, 247, 238, 255)); white.putalpha(rim); white.alpha_composite(big)
    white.save(os.path.join(out, name + '.png')); print(name, white.size)


def registrar(nomes, categoria, ep):
    p = os.path.join(KIT, 'biblioteca', 'indice.json')
    idx = json.load(open(p, encoding='utf-8'))
    for n in nomes:
        idx[n + '.png'] = {'categoria': categoria, 'caminho': f'biblioteca/{categoria}/{n}.png', 'nome_no_codigo': n, 'criado_em': ep}
    json.dump(idx, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('indice ok', len(idx))
