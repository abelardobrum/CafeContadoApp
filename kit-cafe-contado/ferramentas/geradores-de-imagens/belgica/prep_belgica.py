"""Peças novas do EP. 5 Bélgica (Café Contado) — desenhadas em código (MIT)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

BK = (24, 22, 20); YE = (250, 210, 30); RD = (226, 30, 40)


def flag_be():
    """bandeira da Bélgica tremulando num mastro"""
    im, d = canvas(620, 560)
    d.rounded_rectangle(S((40, 30, 62, 540)), radius=S(8), fill=(120, 110, 96))
    d.ellipse(S((32, 14, 70, 52)), fill=(200, 170, 60))
    W, H, x0, y0 = 500, 330, 62, 60
    cols = [BK, YE, RD]
    n = 60
    for i in range(n):
        xa = x0 + W * i / n; xb = x0 + W * (i + 1) / n
        off = lambda x: 16 * math.sin((x - x0) / 95.0)
        c = cols[min(2, int(3 * i / n))]
        shade = 0.86 + 0.14 * math.cos((xa - x0) / 95.0)
        c = tuple(int(v * shade) for v in c)
        d.polygon(S([(xa, y0 + off(xa)), (xb + 1, y0 + off(xb)), (xb + 1, y0 + H + off(xb)), (xa, y0 + H + off(xa))]), fill=c)
    finish(im, 'flag_be', 'objetos')


def porto():
    """guindaste portuário com contêineres empilhados"""
    im, d = canvas(720, 620)
    # guindaste
    d.rectangle(S((90, 120, 120, 560)), fill=(214, 70, 40)); d.rectangle(S((230, 120, 260, 560)), fill=(214, 70, 40))
    d.rectangle(S((60, 110, 660, 150)), fill=(232, 90, 50))
    for i in range(10):
        x = 140 + i * 52
        d.line(S([(x, 110), (x + 26, 150)]), fill=(150, 50, 30), width=S(5))
    d.rectangle(S((140, 60, 220, 110)), fill=(240, 236, 226))
    d.line(S([(520, 150), (520, 300)]), fill=INK, width=S(4))
    d.rectangle(S((450, 300, 590, 360)), fill=(40, 110, 170))
    # contêineres
    cores = [(40, 110, 170), (214, 70, 40), (60, 140, 80), (230, 180, 40), (130, 130, 130), (170, 60, 120)]
    k = 0
    for row in range(3):
        for col in range(3 - (row == 2)):
            x = 300 + col * 135 + (row == 2) * 60; y = 500 - row * 60
            c = cores[k % len(cores)]; k += 1
            d.rectangle(S((x, y, x + 130, y + 56)), fill=c)
            for j in range(8):
                d.line(S([(x + 10 + j * 15, y + 6), (x + 10 + j * 15, y + 50)]), fill=tuple(int(v * 0.72) for v in c), width=S(4))
    d.rectangle(S((30, 560, 700, 600)), fill=(90, 84, 76))
    finish(im, 'porto', 'objetos')


def chart_up():
    """gráfico de preço subindo com seta"""
    im, d = canvas(620, 480)
    d.rounded_rectangle(S((20, 20, 600, 460)), radius=S(24), fill=CREAM)
    d.line(S([(80, 60), (80, 400), (570, 400)]), fill=INK, width=S(8))
    for y in (130, 200, 270, 340):
        d.line(S([(86, y), (560, y)]), fill=(210, 200, 180), width=S(3))
    pts = [(100, 360), (170, 330), (230, 345), (300, 280), (360, 300), (430, 210), (480, 230), (540, 110)]
    d.line(S(pts), fill=(30, 140, 70), width=S(14), joint='curve')
    d.polygon(S([(540, 80), (575, 135), (515, 130)]), fill=(30, 140, 70))
    finish(im, 'chart_up', 'objetos')


def estoque():
    """pilha de sacas com etiqueta de certificado e indicador baixo"""
    im, d = canvas(560, 520)
    juta = (196, 160, 110); juta2 = (170, 134, 88)
    for (x, y) in [(60, 300), (220, 300), (380, 300), (140, 170), (300, 170)]:
        d.rounded_rectangle(S((x, y, x + 150, y + 140)), radius=S(30), fill=juta)
        for j in range(5):
            d.line(S([(x + 15, y + 25 + j * 24), (x + 135, y + 25 + j * 24)]), fill=juta2, width=S(3))
        d.rectangle(S((x + 45, y + 50, x + 105, y + 90)), fill=CREAM)
        d.line(S([(x + 55, y + 64), (x + 95, y + 64)]), fill=INK, width=S(3))
        d.line(S([(x + 55, y + 76), (x + 85, y + 76)]), fill=INK, width=S(3))
    d.ellipse(S((400, 40, 520, 160)), fill=(200, 30, 30))
    d.ellipse(S((412, 52, 508, 148)), fill=(230, 60, 50))
    d.line(S([(435, 100), (455, 125), (495, 70)]), fill=CREAM, width=S(10))
    finish(im, 'estoque', 'objetos')


flag_be(); porto(); chart_up(); estoque()
registrar(['flag_be', 'porto', 'chart_up', 'estoque'], 'objetos', 'BELGICA')
