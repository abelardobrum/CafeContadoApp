"""Peças novas do episódio Café de Morango? (Café Contado) — desenhadas em código (MIT)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM


def morango():
    """morango com sementinhas e folhas"""
    im, d = canvas(420, 480)
    body = [(210, 450)]
    for i in range(0, 181, 6):
        a = math.radians(i)
        # forma de coração invertido arredondado
        x = 210 + math.cos(a) * 180 * (0.75 + 0.25 * math.sin(a))
        y = 170 + math.sin(a) * 40 - 0
        body.append((x, y))
    pts = [(210, 455), (110, 380), (40, 250), (45, 170), (110, 120), (210, 135), (310, 120), (375, 170), (380, 250), (310, 380)]
    d.polygon(S([(x + 8, y + 8) for x, y in pts]), fill=INK)
    d.polygon(S(pts), fill=(212, 34, 40))
    d.polygon(S([(80, 170), (120, 140), (190, 150), (130, 220), (90, 260)]), fill=(240, 90, 90))
    for r in range(6):
        for c in range(7):
            x = 85 + c * 42 + (21 if r % 2 else 0); y = 180 + r * 42
            if 210 - abs(x - 210) * (1 - (y - 140) / 330) < 0: continue
            # dentro do corpo?
            w = 170 * (1 - max(0, (y - 230)) / 230)
            if abs(x - 210) > w - 18: continue
            d.ellipse(S((x - 6, y - 9, x + 6, y + 9)), fill=(250, 220, 90))
            d.ellipse(S((x - 3, y - 5, x + 3, y + 3)), fill=(150, 110, 20))
    for k in range(6):  # sépalas
        a = math.radians(-160 + k * 28)
        tip = (210 + math.cos(a) * 140, 125 + math.sin(a) * 90 + 40)
        d.polygon(S([(210 - 22, 128), tip, (210 + 22, 128)]), fill=(46, 120, 50))
    d.ellipse(S((180, 100, 240, 150)), fill=(36, 100, 40))
    d.line(S([(210, 110), (222, 30)]), fill=(46, 110, 46), width=S(14))
    finish(im, 'morango', 'objetos')


def mirtilo():
    """três mirtilos agrupados"""
    im, d = canvas(420, 360)
    for (x, y, r) in [(140, 210, 110), (290, 220, 100), (215, 120, 90)]:
        d.ellipse(S((x - r + 8, y - r + 8, x + r + 8, y + r + 8)), fill=INK)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=(52, 66, 140))
        d.ellipse(S((x - r * 0.7, y - r * 0.75, x - r * 0.1, y - r * 0.2)), fill=(110, 126, 190))
        # coroinha
        cx, cy = x + r * 0.15, y - r * 0.15
        for k in range(5):
            a = math.radians(k * 72 - 90)
            d.line(S([(cx, cy), (cx + math.cos(a) * 18, cy + math.sin(a) * 18)]), fill=(30, 30, 60), width=S(6))
        d.ellipse(S((cx - 8, cy - 8, cx + 8, cy + 8)), fill=(24, 24, 50))
    finish(im, 'mirtilo', 'objetos')


def molecula():
    """molécula de éster em bolinhas e palitos"""
    im, d = canvas(520, 400)
    at = {'c1': (110, 230, 'C'), 'c2': (220, 170, 'C'), 'o1': (220, 60, 'O'), 'o2': (330, 230, 'O'),
          'c3': (440, 170, 'C'), 'h1': (40, 300, 'H'), 'h2': (60, 150, 'H'), 'h3': (130, 340, 'H'), 'h4': (490, 80, 'H'), 'h5': (490, 260, 'H')}
    bonds = [('c1', 'c2'), ('c2', 'o1'), ('c2', 'o2'), ('o2', 'c3'), ('c1', 'h1'), ('c1', 'h2'), ('c1', 'h3'), ('c3', 'h4'), ('c3', 'h5')]
    for a, b in bonds:
        (x0, y0, _), (x1, y1, _) = at[a], at[b]
        d.line(S([(x0, y0), (x1, y1)]), fill=INK, width=S(18))
        d.line(S([(x0, y0), (x1, y1)]), fill=(200, 196, 186), width=S(10))
    x0, y0, _ = at['c2']; x1, y1, _ = at['o1']
    d.line(S([(x0 + 24, y0), (x1 + 24, y1)]), fill=INK, width=S(12))
    col = {'C': (40, 38, 36), 'O': (214, 40, 40), 'H': (245, 242, 232)}
    rad = {'C': 50, 'O': 48, 'H': 30}
    for x, y, e in at.values():
        r = rad[e]
        d.ellipse(S((x - r - 4, y - r - 4, x + r + 4, y + r + 4)), fill=INK)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=col[e])
        d.ellipse(S((x - r * 0.6, y - r * 0.65, x - r * 0.05, y - r * 0.15)), fill=tuple(min(255, c + 70) for c in col[e]))
    finish(im, 'molecula', 'objetos')


def microbio():
    """microrganismos (leveduras/bactérias) estilizados"""
    im, d = canvas(460, 400)
    # levedura brotando
    for (x, y, rx, ry, colr) in [(170, 200, 120, 100, (230, 196, 90)), (300, 120, 60, 52, (236, 208, 110))]:
        d.ellipse(S((x - rx + 7, y - ry + 7, x + rx + 7, y + ry + 7)), fill=INK)
        d.ellipse(S((x - rx, y - ry, x + rx, y + ry)), fill=colr)
    d.ellipse(S((130, 170, 200, 230)), fill=(170, 120, 50))
    d.ellipse(S((90, 130, 130, 160)), fill=(255, 236, 170))
    # bacilos
    for (x, y, ang) in [(340, 290, 20), (240, 330, -15), (390, 220, 70)]:
        a = math.radians(ang); dx, dy = math.cos(a) * 50, math.sin(a) * 50
        d.line(S([(x - dx + 6, y - dy + 6), (x + dx + 6, y + dy + 6)]), fill=INK, width=S(44))
        d.line(S([(x - dx, y - dy), (x + dx, y + dy)]), fill=(120, 170, 80), width=S(36))
        for e in (-1, 1):
            d.ellipse(S((x + e * dx - 18, y + e * dy - 18, x + e * dx + 18, y + e * dy + 18)), fill=(120, 170, 80))
    finish(im, 'microbio', 'objetos')


morango(); mirtilo(); molecula(); microbio()
registrar(['morango', 'mirtilo', 'molecula', 'microbio'], 'objetos', 'CAFE-DE-MORANGO')
