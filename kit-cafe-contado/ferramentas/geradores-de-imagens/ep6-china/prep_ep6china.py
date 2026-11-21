"""Peças do EP.6 (China): bandeiras tremulando, logo Luckin Coffee, lata de café japonesa. (MIT)"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM, KIT

W, H = 420, 280

def star(d, cx, cy, r, rot, fill):
    pts = []
    for i in range(10):
        a = rot + i * math.pi / 5 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(S(pts), fill=fill)

def flat(draw_fn):
    im, d = canvas(W, H)
    draw_fn(d)
    return im

def wave_and_pole(flag, name):
    a = np.asarray(flag).astype(np.float32)
    h, w = a.shape[:2]
    out = np.zeros((h + 60 * 2, w + 40 * 2, 4), np.float32)
    big = Image.new('RGBA', (out.shape[1], out.shape[0]), (0, 0, 0, 0))
    # onda: deslocamento vertical por coluna + sombreamento
    res = np.zeros((h + 80, w, 4), np.float32)
    for x in range(w):
        ph = x / w
        dy = int(math.sin(ph * 2 * math.pi * 1.2) * 18 * ph * 2 * 1)  # amplitude cresce p/ direita
        shade = 1 - 0.18 * (0.5 + 0.5 * math.cos(ph * 2 * math.pi * 1.2 + 0.6))
        col = a[:, x, :].copy(); col[:, :3] *= shade
        res[40 + dy:40 + dy + h, x, :] = col
    fl = Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))
    pole_w = S(14)
    cw = fl.width + pole_w + S(10)
    ch = fl.height + S(150)
    im = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, S(26), pole_w, ch), fill=(120, 96, 66))
    d.rectangle((pole_w // 2, S(26), pole_w, ch), fill=(90, 70, 48))
    d.ellipse((-S(4), S(10), pole_w + S(4), S(10) + pole_w + S(8)), fill=(214, 172, 60))
    im.alpha_composite(fl, (pole_w + S(4), 0))
    finish(im, name, 'objetos')

def f_br(d):
    d.rectangle(S((0, 0, W, H)), fill=(0, 146, 63))
    d.polygon(S([(W/2, 22), (W-30, H/2), (W/2, H-22), (30, H/2)]), fill=(254, 221, 0))
    d.ellipse(S((W/2-74, H/2-74, W/2+74, H/2+74)), fill=(0, 39, 118))
    d.arc(S((W/2-150, H/2-40, W/2+110, H/2+190)), 215, 300, fill=(255, 255, 255), width=S(14))
def f_cn(d):
    d.rectangle(S((0, 0, W, H)), fill=(222, 41, 16))
    star(d, 70, 70, 44, 0, (255, 222, 0))
    for (x, y, r) in [(140, 28, 0.7), (168, 56, 1.0), (168, 96, 1.4), (140, 124, 1.9)]:
        star(d, x, y, 15, r, (255, 222, 0))
def f_us(d):
    for i in range(13):
        d.rectangle(S((0, i*H/13, W, (i+1)*H/13)), fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle(S((0, 0, W*0.42, H*7/13)), fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            star(d, 16 + c*27 + (r % 2)*6, 15 + r*28, 7, 0, (255, 255, 255))
def f_de(d):
    for i, c in enumerate([(0, 0, 0), (221, 0, 0), (255, 206, 0)]):
        d.rectangle(S((0, i*H/3, W, (i+1)*H/3)), fill=c)
def f_it(d):
    for i, c in enumerate([(0, 146, 70), (244, 245, 240), (206, 43, 55)]):
        d.rectangle(S((i*W/3, 0, (i+1)*W/3, H)), fill=c)
def f_jp(d):
    d.rectangle(S((0, 0, W, H)), fill=(250, 250, 248))
    d.ellipse(S((W/2-84, H/2-84, W/2+84, H/2+84)), fill=(188, 0, 45))
def f_be(d):
    for i, c in enumerate([(0, 0, 0), (253, 218, 36), (239, 51, 64)]):
        d.rectangle(S((i*W/3, 0, (i+1)*W/3, H)), fill=c)

for nm, fn in [('flag_br', f_br), ('flag_cn', f_cn), ('flag_us', f_us), ('flag_de', f_de), ('flag_it', f_it), ('flag_jp', f_jp), ('flag_be', f_be)]:
    wave_and_pole(flat(fn), nm)

def luckin():
    src = Image.open(os.path.join(KIT, 'entrada', 'ep6-china', 'luckin.png')).convert('RGBA')
    a = np.asarray(src).astype(np.int32)
    navy = (a[..., 2] > a[..., 0] + 40) & (a[..., 0] < 120)
    ys, xs = np.where(navy)
    box = (xs.min() - 6, ys.min() - 6, xs.max() + 6, ys.max() + 6)
    im = src.crop(box)
    # fundo branco externo -> transparente (flood fill a partir das bordas)
    rgb = im.convert('RGB'); w, h = rgb.size
    mask = Image.new('L', (w, h), 0)
    for seed in [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1), (w//2, 0), (0, h//2), (w-1, h//2)]:
        ImageDraw.floodfill(rgb, seed, (255, 0, 255), thresh=60)
    arr = np.asarray(rgb)
    out = np.asarray(im).copy()
    out[(arr[..., 0] == 255) & (arr[..., 1] == 0) & (arr[..., 2] == 255), 3] = 0
    lg = Image.fromarray(out)
    sc = 2 * 440 / lg.height
    lg = lg.resize((int(lg.width * sc), int(lg.height * sc)), Image.LANCZOS)
    # placa com nome
    im2, d = canvas(int(lg.width / 2) + 40, 440 + 110)
    im2.alpha_composite(lg, (S(20), 0))
    d.rounded_rectangle(S((10, 452, int(lg.width / 2) + 30, 540)), radius=S(20), fill=(55, 52, 122))
    from PIL import ImageFont
    f = None
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if os.path.exists(p): f = ImageFont.truetype(p, S(50))
    tw = d.textlength('luckin coffee', font=f)
    d.text(((S(int(lg.width / 2) + 40) - tw) / 2, S(466)), 'luckin coffee', fill=(255, 255, 255), font=f)
    finish(im2, 'luckin', 'objetos')

def coffeecan():
    im, d = canvas(260, 440)
    d.rounded_rectangle(S((30, 30, 230, 420)), radius=S(18), fill=(150, 150, 158))
    d.rectangle(S((30, 80, 230, 370)), fill=(110, 58, 30))
    d.rectangle(S((30, 80, 130, 370)), fill=(128, 70, 38))
    d.ellipse(S((30, 14, 230, 50)), fill=(196, 196, 204))
    d.ellipse(S((60, 22, 200, 42)), fill=(170, 170, 178))
    d.rectangle(S((30, 160, 230, 260)), fill=CREAM)
    d.ellipse(S((95, 175, 165, 245)), fill=(188, 0, 45))
    d.ellipse(S((70, 290, 190, 350)), fill=(70, 36, 18))
    d.ellipse(S((86, 300, 174, 340)), fill=(96, 52, 26))
    finish(im, 'coffeecan', 'objetos')

luckin(); coffeecan()
registrar(['flag_br', 'flag_cn', 'flag_us', 'flag_de', 'flag_it', 'flag_jp', 'flag_be', 'luckin', 'coffeecan'], 'objetos', 'EP6-CHINA')
