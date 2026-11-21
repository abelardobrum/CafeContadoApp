"""Peças novas do EP. 4 'O Japão bebeu nosso café de graça!' (Café Contado) — desenhadas em código (MIT)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM
from PIL import ImageFont
RED = (200, 22, 40)

def font(sz):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, S(sz))
    return ImageFont.load_default()

def jpflag():
    """bandeira do Japão ondulada com mastro"""
    im, d = canvas(560, 440)
    d.rounded_rectangle(S((22, 20, 40, 430)), radius=S(8), fill=(120, 90, 60))
    d.ellipse(S((14, 8, 48, 42)), fill=(220, 180, 60))
    W, H, x0, y0 = 480, 300, 40, 50
    top = [(x0 + i, y0 + 14 * math.sin(i / 70)) for i in range(0, W + 1, 8)]
    bot = [(x0 + i, y0 + H + 14 * math.sin(i / 70)) for i in range(W, -1, -8)]
    d.polygon(S([(x+6, y+8) for x, y in top + bot]), fill=INK)
    d.polygon(S(top + bot), fill=(250, 248, 242))
    cx, cy = x0 + W / 2, y0 + H / 2 + 14 * math.sin((W / 2) / 70)
    d.ellipse(S((cx - 90, cy - 90, cx + 90, cy + 90)), fill=RED)
    for i in range(0, W, 120):  # dobras
        d.line(S([(x0 + i + 60, y0 + 10), (x0 + i + 60, y0 + H)]), fill=(225, 222, 214), width=S(4))
    finish(im, 'jpflag', 'objetos')

def jpvending():
    """máquina automática de bebidas (jidōhanbaiki)"""
    im, d = canvas(360, 560)
    d.rounded_rectangle(S((20, 20, 340, 540)), radius=S(18), fill=(30, 90, 170))
    d.rectangle(S((40, 40, 320, 300)), fill=(235, 238, 240))
    cols = [(150, 40, 30), (210, 160, 40), (60, 60, 60), (190, 30, 40), (120, 70, 40), (40, 110, 70)]
    for r in range(3):
        for c in range(5):
            x = 52 + c * 54; y = 52 + r * 82
            col = cols[(r * 5 + c) % len(cols)]
            d.rounded_rectangle(S((x, y, x + 40, y + 62)), radius=S(6), fill=col)
            d.rectangle(S((x + 6, y + 22, x + 34, y + 34)), fill=CREAM)
            d.ellipse(S((x + 14, y + 70, x + 26, y + 78)), fill=(240, 60, 60) if (r + c) % 2 else (60, 200, 90))
    d.rectangle(S((40, 316, 320, 340)), fill=(20, 40, 80))
    d.rectangle(S((250, 360, 310, 440)), fill=(200, 205, 210))
    d.rectangle(S((262, 372, 298, 384)), fill=INK)
    d.rounded_rectangle(S((50, 460, 310, 520)), radius=S(8), fill=(15, 30, 60))
    finish(im, 'jpvending', 'objetos')

def jpcan():
    """lata de café gelado japonês"""
    im, d = canvas(240, 440)
    d.rounded_rectangle(S((30, 40, 210, 420)), radius=S(26), fill=(110, 62, 30))
    d.ellipse(S((30, 20, 210, 70)), fill=(190, 190, 196))
    d.ellipse(S((60, 30, 180, 60)), fill=(160, 160, 168))
    d.rectangle(S((30, 150, 210, 300)), fill=CREAM)
    d.ellipse(S((80, 175, 160, 265)), fill=(110, 62, 30))
    d.line(S([(120, 180), (120, 260)]), fill=CREAM, width=S(5))
    d.text(S((48, 326)), 'COFFEE', font=font(23), fill=CREAM)
    d.rectangle(S((30, 110, 210, 130)), fill=RED)
    d.rectangle(S((56, 40, 76, 420)), fill=(140, 86, 48))
    finish(im, 'jpcan', 'objetos')

def jpcafe():
    """fachada de cafeteria japonesa antiga (lanternas + noren)"""
    im, d = canvas(520, 460)
    d.polygon(S([(10, 120), (260, 30), (510, 120)]), fill=(60, 50, 45))
    d.rectangle(S((40, 120, 480, 440)), fill=(200, 160, 110))
    d.rectangle(S((40, 120, 480, 140)), fill=(120, 80, 50))
    d.rectangle(S((90, 150, 430, 210)), fill=INK)
    d.text(S((150, 160)), 'CAFÉ', font=font(40), fill=(240, 200, 80))
    for i in range(5):  # noren
        x = 110 + i * 62
        d.rectangle(S((x, 230, x + 56, 320)), fill=(30, 60, 120))
    d.ellipse(S((210, 255, 310, 300)), fill=CREAM)
    d.rectangle(S((110, 320, 410, 440)), fill=(90, 60, 40))
    for x in (60, 440):  # lanternas
        d.line(S([(x + 10, 120), (x + 10, 150)]), fill=INK, width=S(3))
        d.ellipse(S((x - 14, 150, x + 34, 230)), fill=RED)
        d.line(S([(x - 10, 190), (x + 30, 190)]), fill=INK, width=S(2))
    finish(im, 'jpcafe', 'objetos')

def instant():
    """pote de café solúvel"""
    im, d = canvas(300, 400)
    d.rounded_rectangle(S((40, 20, 260, 80)), radius=S(10), fill=RED)
    d.rounded_rectangle(S((30, 70, 270, 380)), radius=S(30), fill=(70, 40, 22))
    d.rectangle(S((30, 160, 270, 300)), fill=CREAM)
    d.text(S((52, 200)), 'SOLÚVEL', font=font(34), fill=(70, 40, 22))
    for i in range(10):
        d.ellipse(S((60 + i * 20, 110 + (i % 3) * 10, 72 + i * 20, 122 + (i % 3) * 10)), fill=(130, 80, 40))
    finish(im, 'instant', 'objetos')

jpflag(); jpvending(); jpcan(); jpcafe(); instant()
registrar(["jpflag", "jpvending", "jpcan", "jpcafe", "instant"], "objetos", "JAPAO")
