"""Peças novas do episódio Seu café gera eletricidade (Café Contado) — desenhadas em código (MIT)."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

BR1 = (92, 56, 30); BR2 = (122, 78, 42); BR3 = (150, 100, 58); YEL = (246, 196, 40); RED = (200, 40, 34)


def bean(d, cx, cy, w, h, ang, col=BR1):
    pts = []
    for i in range(36):
        a = i / 36 * 2 * math.pi
        x, y = math.cos(a) * w / 2, math.sin(a) * h / 2
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.polygon(S(pts), fill=col)
    # sulco
    ca, sa = math.cos(ang), math.sin(ang)
    line = []
    for t in range(-10, 11):
        u = t / 10 * w * 0.4; v = math.sin(t / 10 * math.pi) * h * 0.08
        line.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    d.line(S(line), fill=(46, 26, 14), width=S(4))


def moedor():
    """moedor elétrico com pó grudado e faíscas"""
    im, d = canvas(440, 600)
    # funil de grãos (topo)
    d.polygon(S([(110, 30), (330, 30), (280, 170), (160, 170)]), fill=(200, 214, 222))
    d.polygon(S([(125, 42), (315, 42), (272, 160), (168, 160)]), fill=(226, 236, 240))
    random.seed(3)
    for i in range(14):
        bean(d, random.randint(170, 270), random.randint(70, 150), 38, 26, random.random() * 3, random.choice([BR1, BR2]))
    d.rectangle(S((100, 18, 340, 40)), fill=INK)
    # corpo
    d.rounded_rectangle(S((90, 170, 350, 470)), radius=S(30), fill=(48, 44, 42))
    d.rounded_rectangle(S((108, 188, 332, 452)), radius=S(22), fill=(70, 66, 62))
    d.ellipse(S((190, 215, 250, 275)), fill=(150, 150, 150)); d.ellipse(S((204, 229, 236, 261)), fill=(90, 90, 90))
    d.line(S([(220, 232), (220, 246)]), fill=CREAM, width=S(4))
    # bica
    d.rectangle(S((190, 330, 250, 370)), fill=(30, 28, 26))
    # copinho de pó
    d.polygon(S([(130, 420), (310, 420), (290, 580), (150, 580)]), fill=(206, 210, 214))
    d.polygon(S([(146, 432), (294, 432), (278, 568), (162, 568)]), fill=(228, 230, 232))
    d.ellipse(S((150, 400, 290, 460)), fill=BR2)
    # pó grudado na bica e na borda
    for i in range(90):
        x = random.gauss(220, 45); y = random.gauss(400, 25)
        r = random.uniform(2, 6)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=random.choice([BR1, BR2, BR3]))
    for i in range(50):
        x = random.choice([random.uniform(120, 160), random.uniform(280, 320)]); y = random.uniform(420, 540)
        r = random.uniform(2, 5)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=random.choice([BR1, BR2]))
    # faíscas
    for (x, y, s) in [(70, 360, 1.0), (380, 330, 0.8), (380, 470, 0.7)]:
        pts = [(0, -30), (8, -8), (30, 0), (8, 8), (0, 30), (-8, 8), (-30, 0), (-8, -8)]
        d.polygon(S([(x + px * s, y + py * s) for px, py in pts]), fill=YEL)
    finish(im, 'moedor', 'objetos')


def grumos():
    """partículas de pó carregadas formando aglomerados (+ / -)"""
    im, d = canvas(520, 420)
    random.seed(7)
    centers = [(150, 150), (360, 130), (260, 300), (420, 320)]
    for (cx, cy) in centers:
        for i in range(70):
            a = random.random() * 6.283; r = abs(random.gauss(0, 38))
            x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
            rr = random.uniform(5, 11)
            d.ellipse(S((x - rr, y - rr, x + rr, y + rr)), fill=random.choice([BR1, BR2, BR3, (70, 42, 22)]))
    def sign(x, y, plus):
        d.ellipse(S((x - 24, y - 24, x + 24, y + 24)), fill=RED if plus else (40, 90, 170))
        d.line(S([(x - 12, y), (x + 12, y)]), fill=CREAM, width=S(6))
        if plus: d.line(S([(x, y - 12), (x, y + 12)]), fill=CREAM, width=S(6))
    for (x, y, p) in [(90, 70, 1), (230, 90, 0), (440, 60, 1), (180, 380, 0), (480, 220, 1), (60, 280, 0)]:
        sign(x, y, p)
    finish(im, 'grumos', 'objetos')


def canal():
    """corte do café no porta-filtro: água passando por caminhos desiguais"""
    im, d = canvas(520, 520)
    # cesto
    d.polygon(S([(40, 120), (480, 120), (440, 430), (80, 430)]), fill=(170, 172, 176))
    d.polygon(S([(60, 140), (460, 140), (424, 412), (96, 412)]), fill=BR1)
    random.seed(11)
    for i in range(260):
        x = random.uniform(80, 440); y = random.uniform(150, 405)
        r = random.uniform(2, 5)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=random.choice([BR2, (70, 42, 22)]))
    # caminhos (canalização) em azul
    for path, w in [([(150, 140), (170, 220), (140, 300), (165, 412)], 18), ([(330, 140), (300, 230), (345, 330), (320, 412)], 26)]:
        d.line(S(path), fill=(90, 170, 230), width=S(w), joint='curve')
        d.line(S(path), fill=(170, 220, 250), width=S(w // 3), joint='curve')
    # gotas de água em cima
    for x in (120, 200, 260, 320, 400):
        d.polygon(S([(x, 30), (x - 16, 80), (x + 16, 80)]), fill=(90, 170, 230))
        d.ellipse(S((x - 16, 64, x + 16, 96)), fill=(90, 170, 230))
    # gotas saindo irregulares em baixo
    for (x, l) in [(165, 70), (320, 90)]:
        d.line(S([(x, 432), (x, 432 + l)]), fill=(150, 100, 58), width=S(12))
    d.rectangle(S((30, 108, 490, 124)), fill=INK)
    finish(im, 'canal', 'objetos')


def graosagua():
    """punhado de grãos de café com gotinhas de água"""
    im, d = canvas(520, 380)
    random.seed(5)
    for i in range(26):
        x = random.uniform(80, 440); y = random.uniform(140, 330) - (abs(x - 260) * -0.0)
        y = 330 - (1 - ((x - 260) / 190) ** 2) * random.uniform(40, 170)
        bean(d, x, y, 74, 50, random.random() * 3, random.choice([BR1, BR2, (80, 48, 26)]))
    for (x, y) in [(150, 180), (250, 140), (330, 200), (400, 250), (200, 260), (290, 290)]:
        d.polygon(S([(x, y - 30), (x - 13, y + 2), (x + 13, y + 2)]), fill=(120, 190, 240))
        d.ellipse(S((x - 13, y - 10, x + 13, y + 14)), fill=(120, 190, 240))
        d.ellipse(S((x - 5, y - 4, x + 1, y + 4)), fill=(230, 245, 255))
    finish(im, 'graosagua', 'objetos')


def vulcao():
    """vulcão em erupção"""
    im, d = canvas(560, 520)
    # fumaça
    for (x, y, r, c) in [(280, 90, 70, (120, 116, 112)), (210, 70, 55, (140, 136, 130)), (350, 60, 60, (130, 126, 120)), (280, 30, 50, (150, 146, 140))]:
        d.ellipse(S((x - r, y - r * 0.8, x + r, y + r * 0.8)), fill=c)
    # montanha
    d.polygon(S([(20, 500), (220, 170), (340, 170), (540, 500)]), fill=(96, 70, 52))
    d.polygon(S([(280, 500), (300, 170), (340, 170), (540, 500)]), fill=(76, 54, 40))
    # lava
    d.polygon(S([(220, 170), (340, 170), (330, 200), (300, 190), (290, 260), (270, 200), (250, 320), (240, 210)]), fill=(232, 80, 30))
    d.polygon(S([(240, 120), (320, 120), (340, 175), (220, 175)]), fill=(250, 130, 40))
    for (x, y, r) in [(250, 110, 12), (300, 95, 10), (330, 125, 9), (215, 135, 8)]:
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=YEL)
    finish(im, 'vulcao', 'objetos')


def capacete():
    """cientista de vulcão: capacete + óculos (rosto simples)"""
    im, d = canvas(380, 420)
    d.ellipse(S((80, 110, 300, 360)), fill=(232, 190, 150))  # rosto
    d.chord(S((60, 50, 320, 260)), 180, 360, fill=(240, 140, 30))  # capacete
    d.rectangle(S((40, 150, 340, 172)), fill=(210, 110, 20))
    d.rounded_rectangle(S((100, 190, 280, 250)), radius=S(20), fill=(60, 60, 70))
    d.rounded_rectangle(S((112, 200, 182, 240)), radius=S(14), fill=(140, 200, 230))
    d.rounded_rectangle(S((198, 200, 268, 240)), radius=S(14), fill=(140, 200, 230))
    d.arc(S((150, 270, 230, 320)), 20, 160, fill=INK, width=S(6))
    d.rectangle(S((110, 360, 270, 420)), fill=(200, 200, 196))  # jaleco
    finish(im, 'capacete', 'objetos')


moedor(); grumos(); canal(); graosagua(); vulcao(); capacete()
registrar(['moedor', 'grumos', 'canal', 'graosagua', 'vulcao', 'capacete'], 'objetos', 'CAFE-ELETRICIDADE')
