"""Peças novas do EP.3 Expresso italiano (Café Contado) — desenhadas em código (MIT).
bandeiras Itália/Brasil num mastro, lata de café e mistura de grãos (blend)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

GREEN_IT, WHITE_IT, RED_IT = (0, 140, 69), (244, 240, 228), (205, 33, 42)


def wave(x, y, amp=14, w=440):
    return y + amp * math.sin((x / w) * math.pi * 2)


def flag_band(d, x0, x1, y0, y1, color, w=440, amp=14):
    pts = []
    for i in range(21):
        x = x0 + (x1 - x0) * i / 20
        pts.append((x, wave(x, y0, amp, w)))
    for i in range(20, -1, -1):
        x = x0 + (x1 - x0) * i / 20
        pts.append((x, wave(x, y1, amp, w)))
    d.polygon(S(pts), fill=color)


def flag_it():
    """bandeira da Itália tremulando num mastro"""
    im, d = canvas(560, 520)
    d.rectangle(S((40, 30, 58, 500)), fill=INK)
    d.ellipse(S((32, 18, 66, 50)), fill=(220, 180, 60))
    X0, X1, Y0, Y1 = 58, 520, 60, 340
    # sombra
    for (a, b, c) in [(X0, X1, INK)]:
        flag_band(d, a + 10, b + 10, Y0 + 10, Y1 + 10, c)
    w = (X1 - X0) / 3
    for i, col in enumerate([GREEN_IT, WHITE_IT, RED_IT]):
        flag_band(d, X0 + i * w, X0 + (i + 1) * w + 1, Y0, Y1, col)
    finish(im, 'flag_it', 'objetos')


def flag_br():
    """bandeira do Brasil tremulando num mastro"""
    im, d = canvas(560, 520)
    d.rectangle(S((40, 30, 58, 500)), fill=INK)
    d.ellipse(S((32, 18, 66, 50)), fill=(220, 180, 60))
    X0, X1, Y0, Y1 = 58, 520, 60, 340
    flag_band(d, X0 + 10, X1 + 10, Y0 + 10, Y1 + 10, INK)
    flag_band(d, X0, X1, Y0, Y1, (0, 150, 64))
    cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
    ow = lambda x: wave(x, 0)
    d.polygon(S([(X0 + 34, cy + ow(X0 + 34)), (cx, Y0 + 26 + ow(cx)), (X1 - 34, cy + ow(X1 - 34)), (cx, Y1 - 26 + ow(cx))]), fill=(254, 221, 0))
    r = 74
    d.ellipse(S((cx - r, cy - r + ow(cx), cx + r, cy + r + ow(cx))), fill=(0, 39, 118))
    d.arc(S((cx - r - 40, cy - r + 30 + ow(cx), cx + r + 40, cy + r + 150 + ow(cx))), 230, 310, fill=(244, 240, 228), width=S(12))
    for (sx, sy) in [(-30, 30), (10, 44), (36, 22), (-8, 56), (22, 58)]:
        d.ellipse(S((cx + sx - 4, cy + sy - 4 + ow(cx), cx + sx + 4, cy + sy + 4 + ow(cx))), fill=(244, 240, 228))
    finish(im, 'flag_br', 'objetos')


def coffeecan():
    """lata de café genérica (sem marca)"""
    im, d = canvas(400, 520)
    d.rectangle(S((60, 70, 350, 470)), fill=INK)
    d.rectangle(S((50, 60, 340, 460)), fill=(196, 40, 40))
    d.ellipse(S((50, 30, 340, 90)), fill=(170, 170, 176))
    d.ellipse(S((66, 40, 324, 80)), fill=(206, 206, 212))
    d.ellipse(S((50, 430, 340, 490)), fill=(150, 30, 30))
    d.rectangle(S((50, 160, 340, 340)), fill=CREAM)
    d.rectangle(S((50, 168, 340, 176)), fill=(220, 180, 60))
    d.rectangle(S((50, 324, 340, 332)), fill=(220, 180, 60))
    # grão no rótulo
    d.ellipse(S((140, 196, 250, 306)), fill=(92, 54, 30))
    d.arc(S((170, 196, 220, 306)), 270, 90, fill=CREAM, width=S(7))
    for x in range(70, 330, 40):
        d.line(S([(x, 90), (x, 150)]), fill=(214, 70, 64), width=S(4))
    finish(im, 'coffeecan', 'objetos')


def beanmix():
    """mistura de grãos de tons diferentes (blend)"""
    im, d = canvas(560, 400)
    cols = [(64, 36, 20), (110, 64, 34), (150, 96, 52), (88, 50, 26)]
    beans = []
    for i in range(23):
        a = i * 2.399; r = 200 * math.sqrt((i + 0.5) / 23)
        beans.append((280 + math.cos(a) * r, 210 + math.sin(a) * r * 0.62, (i * 37) % 180, cols[i % 4]))
    for (x, y, rot, c) in beans:
        rx, ry = 44, 32
        ang = math.radians(rot)
        pts = [(x + math.cos(t) * rx * math.cos(ang) - math.sin(t) * ry * math.sin(ang),
                y + math.cos(t) * rx * math.sin(ang) + math.sin(t) * ry * math.cos(ang)) for t in [k * math.pi / 16 for k in range(32)]]
        d.polygon(S([(px + 5, py + 5) for px, py in pts]), fill=INK)
        d.polygon(S(pts), fill=c)
        d.line(S([(x - math.cos(ang) * rx * 0.8, y - math.sin(ang) * rx * 0.8),
                  (x + math.cos(ang) * rx * 0.8, y + math.sin(ang) * rx * 0.8)]), fill=(34, 18, 10), width=S(5))
    finish(im, 'beanmix', 'objetos')


flag_it(); flag_br(); coffeecan(); beanmix()
registrar(['flag_it', 'flag_br', 'coffeecan', 'beanmix'], 'objetos', 'EXPRESSO-ITALIANO')
