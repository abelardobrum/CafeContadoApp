"""Peças novas do episódio Café no Espaço (desenhadas em código, MIT).
Saem em biblioteca/espaco/*.png com borda de tesoura branca e halftone leve."""
import math, random, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

OUT = '/home/claude/cr/kit/biblioteca/espaco'
os.makedirs(OUT, exist_ok=True)
SS = 2  # supersample

INK = (28, 24, 20); CREAM = (243, 236, 220); RED = (201, 38, 28); GOLD = (232, 178, 58)
STEEL = (196, 202, 206); STEEL_D = (132, 140, 148); NAVY = (24, 34, 66); BROWN = (92, 52, 26); CREMA = (190, 128, 66)


def canvas(w, h):
    im = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def S(v):
    if isinstance(v, (list, tuple)):
        return [tuple(c * SS for c in x) if isinstance(x, tuple) else x * SS for x in v]
    return v * SS


def tone(im, period=3.6, mix=0.25):
    """halftone leve: pontos escuros proporcionais à sombra, só dentro do alfa"""
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


def finish(im, name, border=3, jag=True):
    im = im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
    im = tone(im, 3.6, 0.45)
    al = im.split()[3]
    pad = border + 6
    big = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    big.paste(im, (pad, pad))
    al = big.split()[3].point(lambda v: 255 if v > 40 else 0)
    rim = al.filter(ImageFilter.MaxFilter(border * 2 + 1))
    if jag:  # borda levemente irregular, como tesoura
        rim = rim.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else 0)
    white = Image.new('RGBA', big.size, (250, 247, 238, 255)); white.putalpha(rim)
    white.alpha_composite(big)
    white.save(f'{OUT}/{name}.png')
    print(name, white.size)


# ---------------------------------------------------------------- fundo do espaço (cenário 1080x1920)
def bg_space():
    rnd = random.Random(3)
    W, H = 1080, 1920
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    top, bot = np.array([14, 18, 40]), np.array([36, 28, 62])
    g = (yy / H)[..., None]
    base[:] = top * (1 - g) + bot * g
    # nebulosas suaves
    for cx, cy, r, col in [(240, 520, 420, (120, 50, 90)), (860, 1350, 520, (40, 80, 120)), (700, 300, 300, (160, 90, 60))]:
        d = np.hypot(xx - cx, yy - cy) / r
        base += np.array(col, np.float32) * np.clip(1 - d, 0, 1)[..., None] ** 2 * 0.55
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
    im = tone(im, 4.2, 0.35)
    d = ImageDraw.Draw(im)
    for i in range(420):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H); r = rnd.choice([1, 1, 1, 1.5, 2, 2.5])
        a = rnd.randint(150, 255)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 248, 225, a))
    for i in range(16):  # estrelas de 4 pontas recortadas
        x, y = rnd.uniform(60, W - 60), rnd.uniform(60, H - 60); r = rnd.uniform(9, 20)
        pts = []
        for k in range(8):
            ang = k * math.pi / 4; rr_ = r if k % 2 == 0 else r * 0.28
            pts.append((x + math.cos(ang) * rr_, y + math.sin(ang) * rr_))
        d.polygon(pts, fill=(255, 236, 190, 255))
    im.convert('RGB').save(f'{OUT}/bg_space.png')
    print('bg_space')


# ---------------------------------------------------------------- estação espacial
def iss():
    w, h = 980, 560
    im, d = canvas(w, h)
    cx, cy = w / 2, h / 2
    # treliça
    d.rectangle(S((40, cy - 14, w - 40, cy + 14)), fill=STEEL_D)
    for x in range(50, w - 40, 26):
        d.line(S((x, cy - 14, x + 26, cy + 14)), fill=(90, 96, 104), width=S(3))
    # painéis solares (8)
    for side in (-1, 1):
        for k in range(2):
            px = cx + side * (210 + k * 150)
            for vy in (-1, 1):
                x0, x1 = px - 58, px + 58
                y0, y1 = (cy - 250, cy - 26) if vy < 0 else (cy + 26, cy + 250)
                d.rectangle(S((x0, y0, x1, y1)), fill=(196, 140, 48))
                for gy in range(int(y0), int(y1), 18): d.line(S((x0, gy, x1, gy)), fill=(120, 80, 28), width=S(2))
                d.line(S((px, y0, px, y1)), fill=(120, 80, 28), width=S(3))
    # módulos centrais
    d.rounded_rectangle(S((cx - 150, cy - 46, cx + 150, cy + 46)), radius=S(40), fill=CREAM)
    d.rounded_rectangle(S((cx - 46, cy - 150, cx + 46, cy + 150)), radius=S(40), fill=(226, 220, 204))
    for x in (cx - 100, cx - 40, cx + 40, cx + 100): d.line(S((x, cy - 44, x, cy + 44)), fill=(170, 164, 150), width=S(3))
    d.ellipse(S((cx - 22, cy - 22, cx + 22, cy + 22)), fill=RED)
    # radiadores
    for sy in (-1, 1):
        d.rectangle(S((cx - 30, cy + sy * 150 - (60 if sy < 0 else 0), cx + 30, cy + sy * 150 + (0 if sy < 0 else 60))), fill=(236, 236, 236))
    finish(im, 'iss')


# ---------------------------------------------------------------- máquina de expresso espacial
def machine(name='spacemachine', steam=False):
    w, h = 520, 560
    im, d = canvas(w, h)
    # corpo
    d.rounded_rectangle(S((40, 60, 480, 520)), radius=S(30), fill=STEEL)
    d.rectangle(S((40, 60, 480, 140)), fill=(170, 176, 184))
    d.rounded_rectangle(S((40, 60, 480, 520)), radius=S(30), outline=(92, 98, 106), width=S(8))
    # faixas de velcro / fixação
    for y in (80, 470):
        d.rectangle(S((40, y, 480, y + 26)), fill=(60, 64, 72))
    # painel
    d.rounded_rectangle(S((300, 170, 450, 300)), radius=S(14), fill=(44, 48, 56))
    for i, col in enumerate([RED, GOLD, (90, 190, 120)]):
        d.ellipse(S((318 + i * 44, 196, 350 + i * 44, 228)), fill=col)
    d.rectangle(S((318, 248, 432, 280)), fill=(110, 200, 210))
    # gaveta de cápsula
    d.rounded_rectangle(S((80, 170, 270, 260)), radius=S(10), fill=(150, 156, 164))
    d.rectangle(S((140, 200, 210, 228)), fill=(80, 84, 92))
    # bico + saída para a bolsa
    d.rectangle(S((140, 300, 210, 380)), fill=(92, 98, 106))
    d.polygon(S([(130, 380), (220, 380), (190, 410), (160, 410)]), fill=(70, 74, 82))
    # bandeirinha italiana (sem marca) e emblema de missão
    d.rectangle(S((300, 330, 330, 370)), fill=(30, 140, 70)); d.rectangle(S((330, 330, 360, 370)), fill=CREAM); d.rectangle(S((360, 330, 390, 370)), fill=RED)
    d.ellipse(S((400, 320, 450, 370)), fill=NAVY); d.ellipse(S((412, 332, 438, 358)), outline=GOLD, width=S(4))
    finish(im, name)


# ---------------------------------------------------------------- astronauta (corpo inteiro, flutuando)
def astronaut(name='astro', arm_up=True):
    w, h = 560, 760
    im, d = canvas(w, h)
    suit, shade = (240, 238, 232), (200, 196, 188)
    # mochila
    d.rounded_rectangle(S((150, 210, 410, 470)), radius=S(30), fill=shade)
    # pernas
    d.rounded_rectangle(S((190, 470, 270, 690)), radius=S(36), fill=suit)
    d.rounded_rectangle(S((290, 470, 370, 680)), radius=S(36), fill=suit)
    d.rounded_rectangle(S((176, 650, 276, 712)), radius=S(22), fill=(80, 84, 92))
    d.rounded_rectangle(S((286, 640, 386, 702)), radius=S(22), fill=(80, 84, 92))
    # tronco
    d.rounded_rectangle(S((170, 250, 390, 500)), radius=S(60), fill=suit)
    d.rounded_rectangle(S((220, 320, 340, 400)), radius=S(10), fill=(210, 206, 198))
    for i, col in enumerate([RED, (60, 140, 220), GOLD]):
        d.rectangle(S((232 + i * 36, 340, 256 + i * 36, 362)), fill=col)
    # braço esquerdo
    d.rounded_rectangle(S((100, 270, 180, 450)), radius=S(36), fill=suit)
    d.ellipse(S((96, 430, 176, 500)), fill=(230, 230, 230))
    # braço direito (levantado)
    if arm_up:
        d.polygon(S([(380, 280), (460, 160), (510, 190), (420, 320)]), fill=suit)
        d.ellipse(S((452, 120, 532, 196)), fill=(230, 230, 230))
    else:
        d.rounded_rectangle(S((380, 270, 460, 450)), radius=S(36), fill=suit)
        d.ellipse(S((384, 430, 464, 500)), fill=(230, 230, 230))
    # bandeira no ombro
    d.rectangle(S((186, 280, 226, 306)), fill=RED)
    # capacete
    d.ellipse(S((170, 40, 390, 260)), fill=suit)
    d.ellipse(S((200, 76, 360, 226)), fill=(40, 56, 96))
    d.ellipse(S((220, 92, 300, 150)), fill=(140, 170, 220))  # reflexo
    d.ellipse(S((300, 170, 330, 196)), fill=(110, 140, 200))
    finish(im, name)


# ---------------------------------------------------------------- bolsa de bebida com canudo
def pouch():
    w, h = 300, 440
    im, d = canvas(w, h)
    d.rounded_rectangle(S((40, 90, 260, 420)), radius=S(26), fill=(236, 232, 222))
    d.rounded_rectangle(S((52, 210, 248, 408)), radius=S(20), fill=BROWN)
    d.rectangle(S((52, 210, 248, 232)), fill=CREMA)
    d.rectangle(S((40, 120, 260, 170)), fill=RED)
    d.rectangle(S((136, 20, 164, 100)), fill=(90, 96, 104))
    d.rectangle(S((128, 84, 172, 104)), fill=(60, 64, 72))
    finish(im, 'pouch')


def capsule():
    w, h = 260, 220
    im, d = canvas(w, h)
    d.polygon(S([(40, 60), (220, 60), (190, 190), (70, 190)]), fill=(150, 30, 34))
    d.rounded_rectangle(S((24, 44, 236, 74)), radius=S(10), fill=(200, 170, 80))
    d.line(S((70, 110, 190, 110)), fill=(120, 20, 24), width=S(6))
    finish(im, 'capsule')


def drops():
    rnd = random.Random(9)
    for n in range(3):
        w = h = 220
        im, d = canvas(w, h)
        cx, cy, r = w / 2, h / 2, 70 + n * 12
        pts = []
        for k in range(48):
            a = k / 48 * 2 * math.pi
            rad = r * (1 + 0.08 * math.sin(3 * a + n) + 0.05 * math.sin(5 * a + 2 * n))
            pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad * 0.92))
        d.polygon(S(pts), fill=BROWN)
        d.ellipse(S((cx - r * 0.55, cy - r * 0.6, cx - r * 0.05, cy - r * 0.2)), fill=(170, 110, 60))
        d.ellipse(S((cx - r * 0.42, cy - r * 0.5, cx - r * 0.22, cy - r * 0.36)), fill=(240, 220, 190))
        finish(im, f'drop{n}')


def socket():
    w, h = 300, 300
    im, d = canvas(w, h)
    d.rounded_rectangle(S((20, 20, 280, 280)), radius=S(36), fill=CREAM)
    d.ellipse(S((70, 70, 230, 230)), fill=(226, 220, 204))
    d.ellipse(S((105, 125, 135, 175)), fill=INK); d.ellipse(S((165, 125, 195, 175)), fill=INK)
    d.ellipse(S((136, 185, 164, 213)), fill=INK)
    finish(im, 'socket')


def coffeemaker():
    w, h = 360, 460
    im, d = canvas(w, h)
    d.rectangle(S((60, 40, 300, 110)), fill=INK)
    d.rectangle(S((240, 110, 300, 400)), fill=INK)
    d.rectangle(S((40, 400, 320, 440)), fill=INK)
    d.polygon(S([(80, 230), (220, 230), (210, 390), (90, 390)]), fill=(200, 220, 230))
    d.rectangle(S((90, 300, 210, 388)), fill=BROWN)
    d.rectangle(S((210, 260, 236, 340)), fill=(60, 60, 60))
    d.rectangle(S((90, 112, 210, 150)), fill=(80, 80, 80))
    d.ellipse(S((262, 70, 282, 90)), fill=RED)
    finish(im, 'coffeemaker')


def gear():
    w = h = 300
    im, d = canvas(w, h)
    cx = cy = 150
    pts = []
    for k in range(48):
        a = k / 48 * 2 * math.pi
        r = 128 if (k // 3) % 2 == 0 else 100
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    d.polygon(S(pts), fill=GOLD)
    d.ellipse(S((cx - 44, cy - 44, cx + 44, cy + 44)), fill=(150, 104, 30))
    d.ellipse(S((cx - 22, cy - 22, cx + 22, cy + 22)), fill=(0, 0, 0, 0))
    finish(im, 'gear')


def flask():
    w, h = 300, 400
    im, d = canvas(w, h)
    d.rectangle(S((120, 30, 180, 150)), fill=(220, 236, 240))
    d.polygon(S([(120, 150), (180, 150), (270, 360), (30, 360)]), fill=(220, 236, 240))
    d.polygon(S([(88, 240), (212, 240), (262, 352), (38, 352)]), fill=BROWN)
    for x, y, r in [(120, 200, 14), (170, 170, 10), (150, 120, 8)]:
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=(170, 110, 60))
    d.rectangle(S((108, 22, 192, 40)), fill=(90, 96, 104))
    finish(im, 'flask')


def clock():
    w = h = 300
    im, d = canvas(w, h)
    d.ellipse(S((20, 20, 280, 280)), fill=CREAM)
    d.ellipse(S((20, 20, 280, 280)), outline=RED, width=S(16))
    for k in range(12):
        a = k / 12 * 2 * math.pi
        d.line(S((150 + math.cos(a) * 100, 150 + math.sin(a) * 100, 150 + math.cos(a) * 118, 150 + math.sin(a) * 118)), fill=INK, width=S(6))
    d.line(S((150, 150, 150, 70)), fill=INK, width=S(10)); d.line(S((150, 150, 210, 170)), fill=INK, width=S(10))
    d.rectangle(S((120, 0, 180, 24)), fill=RED)
    finish(im, 'clock')


def table():
    w, h = 1000, 330
    im, d = canvas(w, h)
    d.rectangle(S((20, 40, 980, 100)), fill=(150, 96, 52))
    d.rectangle(S((20, 40, 980, 56)), fill=(176, 120, 70))
    for x in (60, 900):
        d.rectangle(S((x, 100, x + 40, 320)), fill=(120, 74, 38))
    finish(im, 'table')


bg_space(); iss(); machine(); astronaut('astro', True); astronaut('astro2', False)
pouch(); capsule(); drops(); socket(); coffeemaker(); gear(); flask(); clock(); table()

# registrar no índice da biblioteca
idx_p = '/home/claude/cr/kit/biblioteca/indice.json'
idx = json.load(open(idx_p))
for f in sorted(os.listdir(OUT)):
    idx[f] = {'categoria': 'espaco', 'caminho': f'biblioteca/espaco/{f}', 'nome_no_codigo': f[:-4], 'criado_em': 'CAFE-NO-ESPACO'}
json.dump(idx, open(idx_p, 'w'), ensure_ascii=False, indent=1)
print('indice ok', len(idx))
