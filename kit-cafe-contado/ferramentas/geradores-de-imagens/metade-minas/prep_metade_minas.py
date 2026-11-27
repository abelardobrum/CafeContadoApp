"""Peças novas do episódio "Metade do café do Brasil sai de um estado só" (Café Contado) — desenhadas em código (MIT).
Lavoura (derriça à mão / derriçadeira / pano), terreiro (cenário + rodeiro), calendário da safra,
cheiro, sacaria usada e terreiro mal cuidado."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, tone, INK, CREAM, KIT
from PIL import Image, ImageDraw, ImageFont

FONT = 'C:/Windows/Fonts/impact.ttf'
RED_C = (200, 34, 30); GREEN_C = (128, 168, 56); DRY_C = (62, 36, 24)
LEAF = [(30, 96, 44), (44, 124, 56), (58, 146, 66)]
HAT = (232, 212, 150); HATB = (206, 182, 118); SKIN = (204, 150, 108); PANTS = (40, 52, 84)


def font(px):
    return ImageFont.truetype(FONT, S(px))


def bush(d, cx, cy, w, h, seed=1, fruits=60, trunk=True):
    rnd = random.Random(seed)
    if trunk:
        d.rectangle(S((cx - 10, cy + h * 0.25, cx + 10, cy + h * 0.62)), fill=(110, 72, 40))
    for i in range(46):
        a = rnd.random() * math.tau; r = rnd.random() ** 0.6
        x = cx + math.cos(a) * r * w * 0.42; y = cy + math.sin(a) * r * h * 0.36 - h * 0.05
        rr = rnd.uniform(0.16, 0.24) * w
        d.ellipse(S((x - rr, y - rr * 0.85, x + rr, y + rr * 0.85)), fill=LEAF[i % 3])
    for i in range(fruits):
        a = rnd.random() * math.tau; r = rnd.random() ** 0.7
        x = cx + math.cos(a) * r * w * 0.44; y = cy + math.sin(a) * r * h * 0.36 - h * 0.05
        col = rnd.choice([RED_C, RED_C, RED_C, GREEN_C, DRY_C])
        d.ellipse(S((x - 9, y - 9, x + 9, y + 9)), fill=col)
        d.ellipse(S((x - 5, y - 6, x - 1, y - 2)), fill=tuple(min(255, c + 60) for c in col))


def cherry(d, x, y, col, r=10):
    d.ellipse(S((x - r, y - r, x + r, y + r)), fill=col)
    d.ellipse(S((x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.2)), fill=tuple(min(255, c + 60) for c in col))


def pano(d, x0, x1, y0, y1, seed=3, n=60):
    """pano estendido (trapézio em perspectiva) com frutos caídos"""
    k = (x1 - x0) * 0.12
    d.polygon(S([(x0 + k, y0), (x1 - k, y0), (x1, y1), (x0, y1)]), fill=(236, 228, 206))
    for i in range(1, 4):
        yy = y0 + (y1 - y0) * i / 4
        d.line(S([(x0 + k * (1 - i / 4), yy), (x1 - k * (1 - i / 4), yy)]), fill=(214, 204, 178), width=S(2))
    rnd = random.Random(seed)
    for i in range(n):
        t = rnd.random(); yy = y0 + 8 + t * (y1 - y0 - 16)
        m = k * (1 - t) + 12
        xx = rnd.uniform(x0 + m, x1 - m)
        cherry(d, xx, yy, rnd.choice([RED_C, RED_C, GREEN_C, DRY_C]), 8)


def falling(d, pts, seed=5):
    rnd = random.Random(seed)
    for (x, y) in pts:
        col = rnd.choice([RED_C, RED_C, GREEN_C, DRY_C])
        d.line(S([(x, y - 34), (x, y - 14)]), fill=(90, 80, 70), width=S(3))
        cherry(d, x, y, col, 10)


def person(d, x, y, shirt, arms=None):
    """boneco no estilo worker (chapéu de palha, camisa, calça). x,y = centro dos pés"""
    d.rectangle(S((x - 34, y - 150, x - 6, y)), fill=PANTS)
    d.rectangle(S((x + 6, y - 150, x + 34, y)), fill=PANTS)
    d.rounded_rectangle(S((x - 42, y - 270, x + 42, y - 140)), radius=S(18), fill=shirt)
    d.ellipse(S((x - 34, y - 340, x + 34, y - 268)), fill=SKIN)
    d.ellipse(S((x - 70, y - 334, x + 70, y - 306)), fill=HAT)
    d.rounded_rectangle(S((x - 36, y - 372, x + 36, y - 318)), radius=S(18), fill=HAT)
    d.line(S([(x - 34, y - 326), (x + 34, y - 326)]), fill=HATB, width=S(6))
    for (ax, ay, bx, by) in (arms or []):
        d.line(S([(ax, ay), (bx, by)]), fill=shirt, width=S(20))
        d.ellipse(S((bx - 12, by - 12, bx + 12, by + 12)), fill=SKIN)


# ---------------------------------------------------------------- peças
def derrica():
    """pé de café sendo derriçado: frutos maduros, verdes e secos caindo no pano"""
    im, d = canvas(620, 640)
    pano(d, 40, 580, 470, 620, seed=11, n=70)
    bush(d, 310, 260, 470, 520, seed=4, fruits=80)
    falling(d, [(120, 430), (200, 455), (420, 440), (500, 420), (300, 452), (250, 405), (380, 410), (560, 450)])
    finish(im, 'derrica', 'lavoura-e-clima')


def colhedor_mao():
    """colhedor derriçando o galho com a mão"""
    im, d = canvas(560, 560)
    pano(d, 20, 540, 410, 540, seed=21, n=45)
    bush(d, 340, 230, 380, 420, seed=7, fruits=60)
    person(d, 130, 520, (60, 92, 150), arms=[(150, 300, 250, 210), (110, 300, 215, 250)])
    falling(d, [(240, 300), (270, 360), (230, 390), (300, 330)], seed=8)
    finish(im, 'colhedor_mao', 'objetos')


def derricadeira():
    """colhedor com derriçadeira portátil (vara com motor e pente vibrando)"""
    im, d = canvas(620, 560)
    pano(d, 20, 600, 410, 540, seed=31, n=45)
    bush(d, 420, 220, 380, 420, seed=9, fruits=60)
    person(d, 110, 520, (200, 60, 46), arms=[(130, 300, 170, 330), (95, 300, 150, 300)])
    # vara + motor
    d.line(S([(70, 350), (330, 190)]), fill=(70, 70, 76), width=S(12))
    d.rounded_rectangle(S((40, 330, 110, 380)), radius=S(10), fill=(236, 120, 30))
    d.rectangle(S((52, 342, 98, 352)), fill=INK)
    # pente (dedos)
    for i, a in enumerate((-50, -25, 0, 25, 50)):
        r = math.radians(a - 32)
        d.line(S([(330, 190), (330 + math.cos(r) * 70, 190 + math.sin(r) * 70)]), fill=(40, 40, 44), width=S(7))
    for k in range(3):  # linhas de vibração
        d.arc(S((300 - k * 16, 140 - k * 16, 400 + k * 16, 240 + k * 16)), 200, 260, fill=INK, width=S(4))
    falling(d, [(300, 300), (350, 360), (280, 380), (400, 340), (330, 400)], seed=12)
    finish(im, 'derricadeira', 'objetos')


def rodeiro():
    """trabalhador revirando o café no terreiro com o rodo"""
    im, d = canvas(460, 460)
    # leira de café no chão
    rnd = random.Random(3)
    d.ellipse(S((150, 380, 450, 450)), fill=(92, 52, 32))
    for i in range(140):
        x = rnd.uniform(165, 435); y = rnd.uniform(388, 444)
        if ((x - 300) / 150) ** 2 + ((y - 415) / 35) ** 2 < 1:
            cherry(d, x, y, rnd.choice([(120, 44, 30), (82, 44, 28), (150, 60, 36), DRY_C]), 6)
    # rodo
    d.line(S([(130, 250), (300, 405)]), fill=(150, 104, 58), width=S(10))
    d.rounded_rectangle(S((250, 396, 360, 420)), radius=S(6), fill=(120, 80, 44))
    person(d, 110, 440, (64, 132, 70), arms=[(130, 250, 175, 290), (95, 250, 220, 335)])
    finish(im, 'rodeiro', 'objetos')


def calendario():
    """calendário da safra: MAI a SET; pico JUN–AGO em vermelho"""
    im, d = canvas(940, 300)
    f = font(58); fs = font(26)
    for i, m in enumerate(['MAI', 'JUN', 'JUL', 'AGO', 'SET']):
        x = 20 + i * 182; pico = m in ('JUN', 'JUL', 'AGO')
        d.rectangle(S((x + 6, 46, x + 172, 290)), fill=(60, 50, 40))
        d.rectangle(S((x, 40, x + 166, 284)), fill=(250, 244, 228))
        d.rectangle(S((x, 40, x + 166, 112)), fill=RED_C if pico else (70, 60, 50))
        tw = d.textlength(m, font=f)
        d.text((S(x + 83) - tw / 2, S(44)), m, font=f, fill=(250, 244, 228))
        for r in range(4):
            for c in range(5):
                cx = x + 22 + c * 31; cy = 140 + r * 34
                d.rectangle(S((cx - 9, cy - 9, cx + 9, cy + 9)), fill=(214, 204, 182) if not pico else (238, 190, 170))
        for k in (40, 126):
            d.ellipse(S((x + k - 9, 22, x + k + 9, 58)), outline=INK, width=S(5))
    finish(im, 'calendario', 'objetos')


def wisp(d, x, y, h, col, width=12, phase=0):
    pts = [(x + math.sin(t / 10 + phase) * 22, y - t) for t in range(0, h, 4)]
    d.line(S(pts), fill=col, width=S(width), joint='curve')


def cheiro():
    """fumaça de cheiro (ondas esverdeadas)"""
    im, d = canvas(300, 380)
    for i, (x, ph) in enumerate([(70, 0), (150, 1.4), (230, 2.6)]):
        wisp(d, x, 360, 320, [(120, 150, 60), (150, 170, 70), (100, 130, 50)][i], 16, ph)
    finish(im, 'cheiro', 'objetos')


def sacaria():
    """sacaria reaproveitada de adubo, soltando cheiro"""
    im, d = canvas(420, 520)
    d.polygon(S([(70, 160), (110, 120), (170, 150), (230, 115), (290, 150), (350, 120), (370, 170), (380, 500), (50, 500)]), fill=(196, 160, 104))
    for y in range(180, 500, 14):
        d.line(S([(62, y), (372, y)]), fill=(176, 140, 88), width=S(2))
    d.rectangle(S((100, 260, 330, 400)), outline=(40, 90, 40), width=S(8))
    f = font(66); t = 'ADUBO'
    tw = d.textlength(t, font=f)
    d.text((S(215) - tw / 2, S(290)), t, font=f, fill=(40, 90, 40))
    d.ellipse(S((240, 420, 320, 470)), fill=(150, 116, 70))  # mancha
    for i, (x, ph) in enumerate([(120, 0), (210, 1.6), (300, 2.9)]):
        wisp(d, x, 120, 110, (120, 150, 60), 12, ph)
    finish(im, 'sacaria', 'objetos')


def patio_sujo():
    """pedaço de terreiro mal cuidado: café espalhado com mato, poça e mancha de óleo"""
    im, d = canvas(520, 440)
    d.polygon(S([(70, 120), (450, 120), (510, 420), (10, 420)]), fill=(186, 180, 168))
    for i in range(1, 4):
        y = 120 + i * 75; k = 60 * (1 - i / 4)
        d.line(S([(10 + k, y), (510 - k, y)]), fill=(160, 154, 142), width=S(3))
    for x in (183, 260, 337):
        d.line(S([(x, 120), (x + (x - 260) * 0.6, 420)]), fill=(160, 154, 142), width=S(3))
    d.ellipse(S((60, 300, 220, 370)), fill=(40, 36, 34))      # mancha de óleo
    d.ellipse(S((80, 312, 150, 340)), fill=(80, 70, 90))
    d.ellipse(S((300, 160, 430, 210)), fill=(110, 150, 180))  # poça
    rnd = random.Random(5)
    for i in range(90):
        x = rnd.uniform(200, 470); y = rnd.uniform(240, 400)
        cherry(d, x, y, rnd.choice([(120, 44, 30), (82, 44, 28), DRY_C]), 7)
    for (x, y) in [(60, 200), (440, 300), (250, 140), (120, 410), (470, 400)]:  # mato
        for a in (-30, -10, 10, 30):
            r = math.radians(a - 90)
            d.line(S([(x, y), (x + math.cos(r) * 40, y + math.sin(r) * 40)]), fill=(70, 130, 50), width=S(6))
    for i, (x, ph) in enumerate([(150, 0), (260, 1.5), (370, 2.7)]):
        wisp(d, x, 110, 100, (120, 150, 60), 10, ph)
    finish(im, 'patio_sujo', 'objetos')


def bg_terreiro():
    """cenário: terreiro de café (pátio de cimento com leiras secando ao sol), sede ao fundo"""
    W, H = 1200, 2140
    im = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    for y in range(0, 620):  # céu
        t = y / 620
        d.line([(0, y), (W, y)], fill=(int(150 + 80 * t), int(196 + 34 * t), int(226 + 4 * t)))
    d.polygon([(0, 560), (220, 430), (420, 520), (650, 400), (900, 500), (1200, 420), (1200, 640), (0, 640)], fill=(108, 150, 100))
    # lavoura ao fundo
    for x in range(-20, W + 40, 46):
        d.ellipse((x, 560, x + 50, 610), fill=LEAF[(x // 46) % 3])
    d.rectangle((0, 600, W, 660), fill=(150, 84, 50))
    # sede + tulha
    d.rectangle((120, 520, 380, 640), fill=(246, 240, 226)); d.polygon([(100, 525), (250, 440), (400, 525)], fill=(190, 52, 40))
    for x in (160, 230, 300):
        d.rectangle((x, 560, x + 40, 600), fill=(60, 100, 160))
    d.rectangle((880, 540, 1060, 650), fill=(222, 206, 170)); d.polygon([(860, 545), (970, 480), (1080, 545)], fill=(170, 60, 44))
    d.rectangle((945, 590, 995, 650), fill=(110, 70, 40))
    # pátio em perspectiva
    VX, VY = 600, 300; top = 650
    d.rectangle((0, top, W, H), fill=(196, 190, 176))

    def X(x, y):  # x na linha de base (y=H) -> x na altura y
        return VX + (x - VX) * (y - VY) / (H - VY)
    for xb in range(-2400, 3600, 300):
        d.line([(X(xb, top), top), (xb, H)], fill=(170, 164, 150), width=3)
    # leiras (faixas de café) alternando com cimento, mais grossas embaixo
    rnd = random.Random(2)
    y = top + 10; band = 0
    while y < H:
        hgt = 14 + (y - top) * 0.11
        if band % 2 == 0:
            d.rectangle((0, y, W, y + hgt), fill=(112, 58, 36))
            n = int(W * hgt / 90)
            r = max(2, hgt * 0.09)
            for i in range(n):
                xx = rnd.uniform(0, W); yy = rnd.uniform(y, y + hgt)
                col = rnd.choice([(140, 52, 34), (92, 48, 30), (60, 34, 24), (168, 70, 40), (120, 80, 44)])
                d.ellipse((xx - r, yy - r * 0.8, xx + r, yy + r * 0.8), fill=col)
            # sulcos do rodo
            for k in range(1, 3):
                yy = y + hgt * k / 3
                d.line([(0, yy), (W, yy)], fill=(84, 44, 28), width=max(1, int(hgt * 0.04)))
        else:
            d.line([(0, y), (W, y)], fill=(170, 164, 150), width=2)
        y += hgt * (1.0 if band % 2 == 0 else 0.7); band += 1
    im = tone(im, 3.6, 0.45)
    out = os.path.join(KIT, 'biblioteca', 'cenarios', 'bg_terreiro.png'); im.save(out); print('bg_terreiro', im.size)


derrica(); colhedor_mao(); derricadeira(); rodeiro(); calendario(); cheiro(); sacaria(); patio_sujo(); bg_terreiro()
registrar(['derrica'], 'lavoura-e-clima', 'METADE-DO-CAFE-DO-BRASIL-SAI-DE-UM-ESTADO-SO')
registrar(['colhedor_mao', 'derricadeira', 'rodeiro', 'calendario', 'cheiro', 'sacaria', 'patio_sujo'], 'objetos', 'METADE-DO-CAFE-DO-BRASIL-SAI-DE-UM-ESTADO-SO')
registrar(['bg_terreiro'], 'cenarios', 'METADE-DO-CAFE-DO-BRASIL-SAI-DE-UM-ESTADO-SO')
