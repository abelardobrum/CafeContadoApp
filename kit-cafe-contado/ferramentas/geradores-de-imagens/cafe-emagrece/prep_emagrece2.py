"""Peças novas (rodada 2) do episódio Café emagrece? — cérebro/nervos, câmara calorimétrica, latte com calda, corpos."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

PINK = (236, 150, 160); PINK2 = (214, 112, 128); SKIN = (222, 172, 132); SKIN2 = (196, 142, 104)


def brain():
    """cérebro com nervos descendo (sistema nervoso)"""
    im, d = canvas(460, 520)
    for (x, y, rx, ry) in [(150, 150, 110, 95), (300, 140, 115, 100), (230, 110, 120, 90), (170, 230, 100, 80), (300, 230, 110, 80)]:
        d.ellipse(S((x - rx, y - ry, x + rx, y + ry)), fill=PINK)
    d.line(S([(230, 40), (226, 300)]), fill=PINK2, width=S(8))
    for (x0, y0, k) in [(110, 120, 1), (150, 200, 1), (300, 110, -1), (330, 200, -1), (200, 80, 1), (270, 260, -1), (120, 260, 1)]:
        pts = [(x0 + i * 14 * k, y0 + 10 * math.sin(i * 1.3)) for i in range(6)]
        d.line(S(pts), fill=PINK2, width=S(7), joint='curve')
    d.polygon(S([(205, 290), (255, 290), (248, 500), (212, 500)]), fill=(230, 210, 170))
    for side in (-1, 1):
        for j, y in enumerate((340, 400, 460)):
            d.line(S([(230 + side * 18, y), (230 + side * (90 + j * 20), y + 30), (230 + side * (130 + j * 25), y + 25)]), fill=(246, 196, 40), width=S(6))
    finish(im, 'brain', 'objetos')


def chamber():
    """câmara calorimétrica: cabine de vidro com pessoa sentada e painel de kcal"""
    im, d = canvas(500, 640)
    d.rounded_rectangle(S((20, 20, 480, 620)), radius=S(26), fill=INK)
    d.rounded_rectangle(S((40, 120, 460, 600)), radius=S(16), fill=(190, 222, 228))
    d.rectangle(S((60, 40, 440, 100)), fill=(40, 40, 36))
    for i, h in enumerate((44, 30, 44, 44)):  # display "digitos"
        x = 90 + i * 70
        d.rectangle(S((x, 52, x + 46, 52 + h)), fill=(120, 230, 120))
        d.rectangle(S((x + 8, 60, x + 38, 52 + h - 8)), fill=(40, 40, 36))
    d.ellipse(S((380, 52, 420, 92)), fill=(225, 50, 40))
    d.polygon(S([(70, 140), (140, 140), (60, 330)]), fill=(225, 242, 245))  # reflexo
    d.rectangle(S((150, 470, 360, 500)), fill=(140, 96, 60))  # cadeira
    d.rectangle(S((160, 500, 180, 590)), fill=(110, 74, 46)); d.rectangle(S((330, 500, 350, 590)), fill=(110, 74, 46))
    d.ellipse(S((210, 220, 300, 310)), fill=SKIN)  # cabeça
    d.rounded_rectangle(S((195, 310, 315, 480)), radius=S(36), fill=(70, 110, 160))  # tronco
    d.rounded_rectangle(S((250, 450, 380, 490)), radius=S(18), fill=(50, 60, 90))  # pernas
    d.rectangle(S((350, 460, 380, 580)), fill=(50, 60, 90))
    for k, y in enumerate((170, 200)):  # tubos de ar
        d.line(S([(440, y), (470, y)]), fill=(150, 150, 156), width=S(10))
    finish(im, 'chamber', 'objetos')


def latte():
    """copo de latte com chantilly e calda escorrendo"""
    im, d = canvas(340, 560)
    d.polygon(S([(40, 110), (300, 110), (270, 540), (70, 540)]), fill=(236, 230, 214))
    d.polygon(S([(66, 470), (274, 470), (270, 540), (70, 540)]), fill=(120, 72, 40))
    d.polygon(S([(52, 290), (288, 290), (274, 470), (66, 470)]), fill=(196, 150, 104))
    for (x, y, r) in [(80, 100, 46), (140, 80, 56), (210, 84, 54), (265, 104, 44), (170, 50, 46)]:
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=(252, 250, 244))
    CAR = (178, 96, 30)
    d.line(S([(60, 92), (110, 60), (160, 98), (205, 52), (250, 96), (285, 80)]), fill=CAR, width=S(12), joint='curve')
    for (x, l) in [(70, 120), (150, 170), (240, 90), (285, 140)]:
        d.line(S([(x, 110), (x - 4, 110 + l)]), fill=CAR, width=S(14))
        d.ellipse(S((x - 14, 100 + l, x + 8, 124 + l)), fill=CAR)
    d.polygon(S([(200, 10), (222, 10), (196, 140), (176, 140)]), fill=(225, 50, 40))
    finish(im, 'latte', 'objetos')


def body(name, w):
    """silhueta simples de pessoa (w = meia largura do tronco)"""
    W = 2 * w + 140
    im, d = canvas(W, 640)
    cx = W // 2
    d.ellipse(S((cx - 55, 20, cx + 55, 130)), fill=SKIN)
    d.ellipse(S((cx - 60, 12, cx + 60, 70)), fill=(60, 40, 30))
    d.rectangle(S((cx - 18, 125, cx + 18, 150)), fill=SKIN2)
    d.rounded_rectangle(S((cx - w - 50, 160, cx - w - 6, 420)), radius=S(22), fill=SKIN)
    d.rounded_rectangle(S((cx + w + 6, 160, cx + w + 50, 420)), radius=S(22), fill=SKIN)
    d.rounded_rectangle(S((cx - w, 145, cx + w, 420)), radius=S(int(w * 0.6)), fill=(225, 80, 60))
    lw = max(34, int(w * 0.45))
    d.rounded_rectangle(S((cx - w + 4, 400, cx - 4, 630)), radius=S(16), fill=(50, 60, 90))
    d.rounded_rectangle(S((cx + 4, 400, cx + w - 4, 630)), radius=S(16), fill=(50, 60, 90))
    finish(im, name, 'objetos')


brain(); chamber(); latte(); body('body_thin', 62); body('body_wide', 125)
registrar(['brain', 'chamber', 'latte', 'body_thin', 'body_wide'], 'objetos', 'CAFE-EMAGRECE')
