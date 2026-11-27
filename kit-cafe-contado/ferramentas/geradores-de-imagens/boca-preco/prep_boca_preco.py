"""Peças novas do EP. 2 (A boca que decide o preço do seu café) — classificação do café. Desenhadas em código (MIT)."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM
from PIL import ImageFont

GREEN = (122, 146, 92); GREEN_D = (88, 108, 64)
BROWN = (104, 64, 34); RED = (196, 38, 38)
FONT = 'C:/Windows/Fonts/arialbd.ttf'


def bean(d, cx, cy, w, h, ang, fill, crease=INK, half=None):
    """grão em elipse rotacionada com sulco; half='L'/'R' desenha só metade (quebrado)."""
    pts = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        x, y = math.cos(a) * w / 2, math.sin(a) * h / 2
        if half == 'L' and x > 0: x = 0 + (x * 0.05)
        if half == 'R' and x < 0: x = 0 + (x * 0.05)
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.polygon(S(pts), fill=fill)
    # sulco
    ca, sa = math.cos(ang), math.sin(ang)
    sl = []
    for k in range(11):
        t = -1 + 2 * k / 10
        if (half == 'L' and t > -0.1) or (half == 'R' and t < 0.1): continue
        x, y = t * w * 0.38, math.sin(t * 3) * h * 0.06
        sl.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.line(S(sl), fill=crease, width=S(4))


def pile(name, colors, n=7, seed=1, broken=False):
    im, d = canvas(300, 260)
    rnd = random.Random(seed)
    spots = [(150, 150), (90, 120), (210, 120), (100, 190), (200, 190), (150, 85), (150, 205), (60, 160), (240, 160)][:n]
    for (x, y) in spots:
        c = rnd.choice(colors)
        a = rnd.uniform(-0.8, 0.8)
        if broken:
            lay, ld = canvas(300, 260)
            bean(ld, x, y, 92, 64, a, c)
            ca, sa = math.cos(a), math.sin(a); sgn = rnd.choice((1, -1))
            jag = [(rnd.uniform(-8, 8) + 6 * sgn, t) for t in range(-50, 51, 12)]
            cut = jag + [(sgn * 80, 50), (sgn * 80, -50)]
            ld.polygon(S([(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in cut]), fill=(0, 0, 0, 0))
            im.alpha_composite(lay)
        else:
            bean(d, x, y, 92, 64, a, c)
    finish(im, name, 'objetos')


def def_pedra():
    im, d = canvas(300, 240)
    rnd = random.Random(4)
    for (x, y, r) in [(100, 140, 62), (200, 150, 52), (150, 90, 44), (230, 80, 30), (70, 70, 28)]:
        pts = [(x + math.cos(a) * r * rnd.uniform(0.75, 1.1), y + math.sin(a) * r * 0.8 * rnd.uniform(0.75, 1.1))
               for a in [i * math.pi / 5 for i in range(10)]]
        g = rnd.randint(120, 150)
        d.polygon(S(pts), fill=(g, g - 4, g - 12))
        d.ellipse(S((x - r * 0.4, y - r * 0.45, x - r * 0.05, y - r * 0.2)), fill=(g + 40, g + 36, g + 28))
    finish(im, 'def_pedra', 'objetos')


def def_pau():
    im, d = canvas(320, 240)
    for (x0, y0, x1, y1, w) in [(40, 180, 280, 70, 18), (60, 90, 260, 200, 14), (120, 40, 200, 220, 10)]:
        d.line(S([(x0, y0), (x1, y1)]), fill=(122, 86, 50), width=S(w))
        d.line(S([(x0 + 3, y0 - 3), (x1 + 3, y1 - 3)]), fill=(160, 120, 76), width=S(max(3, w // 4)))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        d.line(S([(mx, my), (mx + 30, my - 34)]), fill=(122, 86, 50), width=S(w // 2 + 2))
    finish(im, 'def_pau', 'objetos')


def def_casca():
    """cascas secas do fruto (metades murchas)"""
    im, d = canvas(300, 250)
    rnd = random.Random(7)
    for (x, y) in [(95, 110), (200, 95), (150, 175), (235, 180), (70, 190)]:
        a = rnd.uniform(-0.6, 0.6)
        ca, sa = math.cos(a), math.sin(a)
        rot = lambda px, py: (x + px * ca - py * sa, y + px * sa + py * ca)
        outer = [rot(math.cos(t) * 50 * rnd.uniform(0.92, 1.05), math.sin(t) * 38 * rnd.uniform(0.92, 1.05))
                 for t in [i * math.pi / 12 for i in range(24)]]
        d.polygon(S(outer), fill=(118, 52, 36))
        inner = [rot(math.cos(t) * 34, math.sin(t) * 22 + 4) for t in [i * math.pi / 12 for i in range(24)]]
        d.polygon(S(inner), fill=(196, 150, 100))
        d.line(S([rot(-20, -14), rot(8, -20), rot(26, -10)]), fill=(80, 34, 22), width=S(3))
    finish(im, 'def_casca', 'objetos')


def amostra():
    """balança de prato com montinho de café verde e visor 300 g"""
    im, d = canvas(460, 420)
    d.rounded_rectangle(S((40, 230, 420, 400)), radius=S(30), fill=(214, 212, 204))
    d.rounded_rectangle(S((60, 250, 400, 380)), radius=S(22), fill=(236, 234, 226))
    d.rounded_rectangle(S((140, 290, 320, 360)), radius=S(10), fill=INK)
    f = ImageFont.truetype(FONT, S(48))
    d.text(S((230, 326)), '300 g', fill=(120, 230, 120), font=f, anchor='mm')
    d.rectangle(S((215, 200, 245, 235)), fill=(150, 150, 150))
    d.ellipse(S((60, 170, 400, 230)), fill=(170, 170, 176))
    d.ellipse(S((76, 176, 384, 220)), fill=(200, 200, 206))
    rnd = random.Random(3)
    for i in range(70):
        a = i * 2.399; r = 135 * math.sqrt(i / 70)
        x = 230 + math.cos(a) * r
        y = 168 - (1 - (r / 135) ** 2) * 120 + math.sin(a) * 18
        bean(d, x, y, 40, 28, rnd.uniform(-1, 1), rnd.choice([GREEN, GREEN_D, (138, 160, 104)]))
    finish(im, 'amostra', 'objetos')


def peneira():
    """peneira redonda vista de cima (aro de madeira, furos), com grãos"""
    im, d = canvas(500, 420)
    d.ellipse(S((20, 40, 480, 400)), fill=(150, 104, 60))
    d.ellipse(S((44, 62, 456, 378)), fill=(176, 128, 78))
    d.ellipse(S((60, 74, 440, 366)), fill=(150, 152, 156))
    for row in range(14):
        for col in range(20):
            x = 74 + col * 19 + (row % 2) * 9; y = 88 + row * 20
            if ((x - 250) / 190) ** 2 + ((y - 220) / 146) ** 2 < 0.9:
                d.ellipse(S((x - 6, y - 6, x + 6, y + 6)), fill=(60, 62, 66))
    rnd = random.Random(9)
    for i in range(16):
        a = i * 2.399; r = 120 * math.sqrt(i / 16)
        bean(d, 250 + math.cos(a) * r, 220 + math.sin(a) * r * 0.7, 46, 32, rnd.uniform(-1, 1),
             rnd.choice([GREEN, GREEN_D]))
    finish(im, 'peneira', 'objetos')


def boca():
    """lábios provando café na colher de prova (o provador)"""
    im, d = canvas(520, 400)
    # colher de prova
    d.line(S([(300, 250), (500, 360)]), fill=(150, 150, 158), width=S(24))
    d.ellipse(S((150, 200, 330, 300)), fill=(150, 150, 158))
    d.ellipse(S((164, 210, 316, 288)), fill=(92, 52, 26))
    d.ellipse(S((190, 222, 250, 244)), fill=(140, 90, 50))
    # lábios
    up = [(60, 150), (110, 105), (160, 92), (200, 112), (240, 92), (290, 105), (340, 150), (200, 160)]
    lo = [(60, 150), (200, 160), (340, 150), (300, 196), (200, 214), (100, 196)]
    d.polygon(S(up), fill=RED)
    d.polygon(S(lo), fill=(214, 60, 58))
    d.line(S([(60, 150), (130, 154), (200, 162), (270, 154), (340, 150)]), fill=(110, 20, 24), width=S(7))
    d.ellipse(S((170, 172, 240, 190)), fill=(240, 120, 110))
    finish(im, 'boca', 'objetos')


def chaleira():
    """chaleira despejando água quente"""
    im, d = canvas(460, 400)
    d.polygon(S([(90, 330), (120, 150), (320, 150), (350, 330)]), fill=(196, 44, 40))
    d.rounded_rectangle(S((80, 320, 360, 350)), radius=S(10), fill=(150, 30, 30))
    d.ellipse(S((170, 120, 270, 160)), fill=(150, 30, 30))
    d.ellipse(S((205, 100, 235, 125)), fill=INK)
    d.arc(S((130, 40, 310, 230)), 200, 340, fill=INK, width=S(14))
    d.polygon(S([(330, 250), (430, 170), (445, 185), (350, 290)]), fill=(196, 44, 40))
    for k in range(8):
        y = 200 + k * 26
        d.ellipse(S((430 - 8 + k * 2, y - 10, 430 + 8 + k * 2, y + 10)), fill=(120, 180, 230))
    for x0 in (180, 230, 280):
        pts = [(x0 + math.sin(k / 2) * 10, 95 - k * 7) for k in range(10)]
        d.line(S(pts), fill=(220, 220, 220), width=S(6))
    finish(im, 'chaleira', 'objetos')


pile('def_preto', [(34, 30, 28), (48, 42, 38), (24, 22, 22)], seed=1)
pile('def_ardido', [(196, 140, 60), (176, 112, 48), (206, 160, 80)], seed=2)
pile('def_quebrado', [GREEN, GREEN_D, (138, 160, 104)], seed=3, broken=True)
def_pedra(); def_pau(); def_casca(); amostra(); peneira(); boca(); chaleira()
registrar(['def_preto', 'def_ardido', 'def_quebrado', 'def_pedra', 'def_pau', 'def_casca',
           'amostra', 'peneira', 'boca', 'chaleira'], 'objetos', 'A-BOCA-QUE-DECIDE-O-PRECO-DO-SEU-CAFE')
