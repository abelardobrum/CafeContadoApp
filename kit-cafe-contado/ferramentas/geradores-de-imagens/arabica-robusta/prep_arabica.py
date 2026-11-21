"""Peças novas do episódio Arábica x Robusta (Café Contado) — desenhadas em código (MIT).
Saem em biblioteca/amazonia/*.png com borda de tesoura branca e halftone leve."""
import math, random, os, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(KIT, 'biblioteca', 'amazonia')
os.makedirs(OUT, exist_ok=True)
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
    rad = np.sqrt(np.clip(1 - lum, 0, 1)) * 0.55
    dot = (d < rad).astype(np.float32)
    rgb = rgb * (1 - mix * dot[..., None] * 0.55)
    return Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), al], -1).astype(np.uint8))


def finish(im, name, border=3):
    im = im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
    im = tone(im, 3.6, 0.45)
    pad = border + 6
    big = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    big.paste(im, (pad, pad))
    al = big.split()[3].point(lambda v: 255 if v > 40 else 0)
    rim = al.filter(ImageFilter.MaxFilter(border * 2 + 1))
    rim = rim.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else 0)
    white = Image.new('RGBA', big.size, (250, 247, 238, 255)); white.putalpha(rim)
    white.alpha_composite(big)
    white.save(f'{OUT}/{name}.png'); print(name, white.size)


def bg_amazonia():
    """floresta em camadas recortadas + rio sinuoso + céu quente (1080x1920)"""
    rnd = random.Random(7)
    W, H = 1080, 1920
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = (yy / H)[..., None]
    sky = np.array([238, 214, 160]) * (1 - g) + np.array([214, 168, 104]) * g
    im = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im)
    d.ellipse((640, 170, 900, 430), fill=(246, 196, 92))  # sol
    layers = [(560, (96, 128, 78)), (760, (66, 108, 58)), (980, (44, 88, 46)), (1220, (30, 70, 38))]
    for li, (base, col) in enumerate(layers):
        pts = [(0, H)]
        x = -40
        while x < W + 80:
            r = rnd.uniform(60, 120) * (1 + li * 0.25)
            for a in range(0, 181, 15):
                ang = math.radians(180 - a)
                pts.append((x + r + math.cos(ang) * r, base - math.sin(ang) * r * rnd.uniform(0.7, 1.0) + rnd.uniform(-6, 6)))
            x += r * 1.6
        pts.append((W, H))
        d.polygon(pts, fill=col + (255,))
        # árvores emergentes (castanheiras) na camada do fundo
        if li == 1:
            for tx in (180, 820):
                d.rectangle((tx - 9, base - 260, tx + 9, base), fill=(70, 52, 34))
                d.ellipse((tx - 120, base - 360, tx + 120, base - 220), fill=(78, 116, 64))
    # rio
    rpts_l, rpts_r = [], []
    for i in range(0, 41):
        y = 1180 + i * 19
        cx = 540 + math.sin(i * 0.25) * 170
        wdt = 30 + i * 9
        rpts_l.append((cx - wdt, y)); rpts_r.append((cx + wdt, y))
    d.polygon(rpts_l + rpts_r[::-1], fill=(126, 156, 150))
    for i in range(14):
        y = rnd.uniform(1250, 1900); x = 540 + math.sin((y - 1180) / 19 * 0.25) * 170
        d.line((x - 40, y, x + 40, y), fill=(196, 214, 204), width=4)
    # folhagem de primeiro plano
    for i in range(26):
        side = i % 2
        x0 = rnd.uniform(-40, 220) if side == 0 else rnd.uniform(860, 1120)
        y0 = rnd.uniform(1450, 1960)
        L = rnd.uniform(160, 300); ang = math.radians(rnd.uniform(-70, -20) if side == 0 else rnd.uniform(-160, -110))
        x1, y1 = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L
        nx, ny = -math.sin(ang) * L * 0.18, math.cos(ang) * L * 0.18
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        d.polygon([(x0, y0), (mx + nx, my + ny), (x1, y1), (mx - nx, my - ny)], fill=(rnd.randint(20, 40), rnd.randint(78, 108), rnd.randint(36, 52), 255))
    im = tone(im, 4.2, 0.35)
    im.convert('RGB').save(f'{OUT}/bg_amazonia.png'); print('bg_amazonia')


def castanha():
    """ouriço da castanha-do-pará aberto, com castanhas"""
    im, d = canvas(460, 380)
    d.ellipse(S((40, 60, 400, 360)), fill=(104, 64, 34))
    d.ellipse(S((70, 80, 370, 330)), fill=(138, 88, 48))
    d.ellipse(S((120, 120, 320, 300)), fill=(236, 214, 170))
    rnd = random.Random(2)
    for i in range(6):  # castanhas em gomos
        a = i * math.pi / 3
        cx, cy = 220 + math.cos(a) * 55, 210 + math.sin(a) * 50
        pts = [(cx + math.cos(a) * 42, cy + math.sin(a) * 42), (cx + math.cos(a + 2.1) * 26, cy + math.sin(a + 2.1) * 26), (cx + math.cos(a - 2.1) * 26, cy + math.sin(a - 2.1) * 26)]
        d.polygon(S(pts), fill=(92, 56, 30))
        d.line(S([pts[0], (cx, cy)]), fill=(150, 104, 62), width=S(3))
    for x, y in [(380, 300), (430, 250)]:  # castanhas soltas
        d.polygon(S([(x - 30, y + 20), (x, y - 38), (x + 30, y + 20)]), fill=(92, 56, 30))
    finish(im, 'castanha')


def chocolate():
    im, d = canvas(380, 460)
    d.polygon(S([(40, 160), (340, 160), (340, 440), (40, 440)]), fill=(196, 38, 30))  # papel
    d.rectangle(S((40, 160, 340, 220)), fill=(232, 178, 58))
    d.polygon(S([(40, 40), (340, 40), (340, 180), (300, 160), (260, 190), (210, 165), (160, 195), (100, 168), (40, 190)]), fill=(86, 46, 24))
    for gx in range(2):
        for gy in range(2):
            x0, y0 = 60 + gx * 140, 52 + gy * 58
            d.rectangle(S((x0, y0, x0 + 124, y0 + 46)), fill=(108, 60, 32))
            d.rectangle(S((x0 + 6, y0 + 6, x0 + 118, y0 + 40)), fill=(96, 52, 28))
    d.text(S((120, 290)), ' ', fill=CREAM)
    finish(im, 'chocolate')


def frutas():
    """cacho de frutinhas vermelhas e roxas (notas frutadas)"""
    im, d = canvas(420, 400)
    rnd = random.Random(5)
    d.line(S([(210, 20), (210, 120)]), fill=(70, 96, 46), width=S(10))
    d.polygon(S([(210, 60), (330, 20), (290, 100)]), fill=(70, 120, 56))
    d.polygon(S([(210, 70), (90, 30), (130, 110)]), fill=(56, 104, 48))
    pts = [(210, 170), (150, 200), (270, 200), (110, 260), (210, 250), (310, 260), (160, 310), (260, 310), (210, 350), (90, 330), (330, 330)]
    for i, (x, y) in enumerate(pts):
        col = [(196, 30, 34), (126, 34, 82), (220, 64, 44)][i % 3]
        r = rnd.uniform(40, 52)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=col)
        d.ellipse(S((x - r * 0.5, y - r * 0.6, x - r * 0.15, y - r * 0.25)), fill=(250, 220, 210))
    finish(im, 'frutas')


bg_amazonia(); castanha(); chocolate(); frutas()

idx_p = os.path.join(KIT, 'biblioteca', 'indice.json')
idx = json.load(open(idx_p, encoding='utf-8'))
for f in sorted(os.listdir(OUT)):
    idx[f] = {'categoria': 'amazonia', 'caminho': f'biblioteca/amazonia/{f}', 'nome_no_codigo': f[:-4], 'criado_em': 'ARABICA-X-ROBUSTA'}
json.dump(idx, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('indice ok', len(idx))
