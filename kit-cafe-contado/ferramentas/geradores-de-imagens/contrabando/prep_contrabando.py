"""Peças novas do episódio Café de contrabando (Café Contado) — desenhadas em código (MIT).
Saem em biblioteca/objetos/*.png."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

GREEN = (46, 110, 52); GREEN2 = (70, 140, 66); DGREEN = (30, 78, 38)
RED = (196, 38, 34); GOLD = (232, 182, 52); KRAFT = (196, 152, 98); KRAFT2 = (170, 126, 76)


def leaf(d, cx, cy, L, W, ang, col):
    """folha elíptica pontuda girada"""
    pts = []
    for i in range(41):
        v = i / 40 * 2 * math.pi
        x = math.cos(v) * L / 2
        y = math.sin(v) * W / 2 * (1 - 0.35 * math.cos(v))
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.polygon(S(pts), fill=col)
    ca, sa = math.cos(ang), math.sin(ang)
    d.line(S([(cx - L / 2 * ca, cy - L / 2 * sa), (cx + L / 2 * 0.8 * ca, cy + L / 2 * 0.8 * sa)]), fill=DGREEN, width=S(2))


def seedling(d, x, ybase, h, lean=0):
    top = (x + lean, ybase - h)
    d.line(S([(x, ybase), top]), fill=(92, 120, 50), width=S(7))
    for k, f in enumerate((0.35, 0.62, 0.88)):
        px, py = x + lean * f, ybase - h * f
        sz = 1.0 - 0.18 * k
        leaf(d, px - 34 * sz, py - 8, 70 * sz, 30 * sz, -0.35, GREEN if k % 2 else GREEN2)
        leaf(d, px + 34 * sz, py - 8, 70 * sz, 30 * sz, math.pi + 0.35, GREEN2 if k % 2 else GREEN)
    leaf(d, top[0], top[1] - 14, 40, 20, -math.pi / 2, GREEN2)


def flower(d, cx, cy, r, petal, center):
    for i in range(8):
        a = i / 8 * 2 * math.pi
        px, py = cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62
        d.ellipse(S((px - r * 0.48, py - r * 0.48, px + r * 0.48, py + r * 0.48)), fill=petal)
    d.ellipse(S((cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4)), fill=center)


def buque():
    """buquê de flores com mudas de café escondidas no meio"""
    im, d = canvas(480, 640)
    # folhagem de fundo
    for (x, y, a) in [(110, 250, -2.4), (370, 250, -0.7), (90, 330, -2.9), (390, 330, -0.2)]:
        leaf(d, x, y, 120, 46, a, DGREEN)
    # mudas de café (mais altas, no meio)
    seedling(d, 240, 330, 250, 0)
    seedling(d, 195, 340, 200, -30)
    seedling(d, 288, 340, 205, 32)
    # flores em volta
    for (x, y, r, p, c) in [(120, 300, 58, (238, 120, 150), (250, 220, 90)), (360, 300, 58, (250, 250, 244), (240, 190, 60)),
                            (170, 360, 52, (246, 196, 60), (190, 90, 40)), (310, 360, 52, (226, 80, 96), (250, 220, 90)),
                            (240, 385, 46, (250, 250, 244), (240, 190, 60)), (75, 375, 40, (246, 196, 60), (190, 90, 40)),
                            (405, 375, 40, (238, 120, 150), (250, 220, 90))]:
        flower(d, x, y, r, p, c)
    # cone de papel kraft
    d.polygon(S([(40, 380), (440, 380), (262, 630), (218, 630)]), fill=KRAFT)
    d.polygon(S([(40, 380), (240, 380), (218, 630)]), fill=KRAFT2)
    d.line(S([(40, 380), (440, 380)]), fill=INK, width=S(4))
    # laço vermelho
    d.polygon(S([(240, 520), (160, 480), (170, 560)]), fill=RED)
    d.polygon(S([(240, 520), (320, 480), (310, 560)]), fill=RED)
    d.polygon(S([(232, 524), (200, 610), (222, 604)]), fill=(160, 26, 24))
    d.polygon(S([(248, 524), (280, 610), (258, 604)]), fill=(160, 26, 24))
    d.ellipse(S((222, 502, 258, 538)), fill=(160, 26, 24))
    finish(im, 'buque', 'objetos')


def marco():
    """marco de pedra português (padrão) com cruz e escudo"""
    im, d = canvas(300, 620)
    # torrão de terra na base
    d.ellipse(S((30, 520, 270, 610)), fill=(110, 76, 44))
    d.ellipse(S((60, 530, 240, 590)), fill=(132, 92, 54))
    # coluna
    d.polygon(S([(95, 200), (205, 200), (220, 560), (80, 560)]), fill=(176, 172, 160))
    d.polygon(S([(150, 200), (205, 200), (220, 560), (150, 560)]), fill=(150, 146, 136))
    d.rectangle(S((80, 180, 220, 210)), fill=(196, 192, 180))
    # cruz no topo
    d.rectangle(S((136, 30, 164, 185)), fill=(196, 192, 180))
    d.rectangle(S((95, 75, 205, 103)), fill=(196, 192, 180))
    d.rectangle(S((140, 34, 160, 181)), fill=RED); d.rectangle(S((99, 79, 201, 99)), fill=RED)
    # escudo português (quinas)
    d.polygon(S([(110, 260), (190, 260), (190, 330), (150, 370), (110, 330)]), fill=(250, 247, 238))
    d.polygon(S([(118, 268), (182, 268), (182, 326), (150, 358), (118, 326)]), fill=(28, 70, 150))
    for (x, y) in [(150, 285), (130, 312), (150, 312), (170, 312), (150, 338)]:
        d.rectangle(S((x - 6, y - 8, x + 6, y + 8)), fill=(250, 247, 238))
    # rachaduras
    d.line(S([(110, 420), (130, 450), (122, 480)]), fill=(110, 106, 98), width=S(3))
    d.line(S([(190, 400), (175, 440)]), fill=(110, 106, 98), width=S(3))
    finish(im, 'marco', 'objetos')


def palheta():
    """oficial português do séc. XVIII (busto): tricórnio, peruca, casaca"""
    im, d = canvas(460, 560)
    BLUE = (34, 58, 120); SKIN = (232, 188, 150); WIG = (236, 232, 222)
    # casaca
    d.polygon(S([(40, 560), (70, 400), (160, 350), (300, 350), (390, 400), (420, 560)]), fill=BLUE)
    d.polygon(S([(160, 350), (230, 470), (200, 560), (150, 560), (130, 420)]), fill=RED)
    d.polygon(S([(300, 350), (230, 470), (260, 560), (310, 560), (330, 420)]), fill=RED)
    d.polygon(S([(200, 350), (260, 350), (230, 470)]), fill=(250, 247, 238))  # jabô
    for y in (420, 470, 520):
        d.ellipse(S((160, y, 178, y + 18)), fill=GOLD); d.ellipse(S((282, y, 300, y + 18)), fill=GOLD)
    # dragonas
    d.ellipse(S((50, 370, 150, 420)), fill=GOLD); d.ellipse(S((310, 370, 410, 420)), fill=GOLD)
    # pescoço e rosto
    d.rectangle(S((200, 300, 260, 360)), fill=SKIN)
    # peruca (cachos laterais)
    for y in (220, 262, 304):
        d.ellipse(S((128, y, 176, y + 46)), fill=WIG); d.ellipse(S((284, y, 332, y + 46)), fill=WIG)
    d.ellipse(S((150, 140, 310, 330)), fill=SKIN)
    # olhos, sobrancelhas, bigode
    d.ellipse(S((188, 215, 206, 233)), fill=INK); d.ellipse(S((254, 215, 272, 233)), fill=INK)
    d.line(S([(180, 200), (210, 196)]), fill=(90, 60, 40), width=S(6)); d.line(S([(250, 196), (280, 200)]), fill=(90, 60, 40), width=S(6))
    d.polygon(S([(230, 230), (220, 268), (240, 268)]), fill=(214, 166, 128))
    d.arc(S((205, 270, 255, 300)), 20, 160, fill=(150, 60, 50), width=S(5))
    # tricórnio
    d.polygon(S([(100, 170), (230, 70), (360, 170), (300, 150), (230, 165), (160, 150)]), fill=INK)
    d.line(S([(100, 170), (160, 150), (230, 165), (300, 150), (360, 170)]), fill=GOLD, width=S(6))
    d.ellipse(S((214, 120, 246, 152)), fill=RED)  # laço/cocar
    finish(im, 'palheta', 'objetos')


def livro():
    """livro de romance (capa vermelha com coração)"""
    im, d = canvas(420, 480)
    d.polygon(S([(70, 60), (360, 40), (380, 420), (90, 450)]), fill=(240, 232, 212))  # páginas
    d.polygon(S([(50, 50), (340, 30), (360, 410), (70, 440)]), fill=(150, 30, 40))
    d.polygon(S([(50, 50), (90, 47), (110, 437), (70, 440)]), fill=(110, 20, 28))  # lombada
    for y in (80, 395):
        d.line(S([(110, y), (330, y - 18)]), fill=GOLD, width=S(5))
    # coração
    cx, cy = 225, 230
    pts = []
    for i in range(80):
        t = i / 80 * 2 * math.pi
        x = 16 * math.sin(t) ** 3; y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * 5.4, cy + y * 5.4))
    d.polygon(S(pts), fill=GOLD)
    d.polygon(S([(300, 30), (322, 28), (330, 120), (318, 104), (306, 122)]), fill=GOLD)  # marcador
    finish(im, 'livro', 'objetos')


def pergaminho():
    """ordem secreta: pergaminho com selo de cera"""
    im, d = canvas(460, 380)
    d.rectangle(S((70, 60, 390, 320)), fill=(238, 220, 178))
    d.ellipse(S((40, 40, 100, 340)), fill=(214, 190, 140)); d.ellipse(S((360, 40, 420, 340)), fill=(214, 190, 140))
    d.ellipse(S((55, 50, 85, 330)), fill=(190, 164, 116)); d.ellipse(S((375, 50, 405, 330)), fill=(190, 164, 116))
    for i, y in enumerate(range(100, 260, 30)):
        d.line(S([(115, y), (345 - (i % 3) * 40, y)]), fill=(90, 70, 50), width=S(5))
    d.ellipse(S((270, 230, 350, 310)), fill=RED)
    d.ellipse(S((284, 244, 336, 296)), fill=(160, 26, 24))
    d.line(S([(298, 270), (322, 270)]), fill=(220, 90, 80), width=S(5)); d.line(S([(310, 258), (310, 282)]), fill=(220, 90, 80), width=S(5))
    finish(im, 'pergaminho', 'objetos')


def dama():
    """dama do séc. XVIII (busto): penteado alto empoado, vestido rosa, leque"""
    im, d = canvas(440, 600)
    SKIN = (238, 196, 160); WIG = (240, 236, 228); PINK = (226, 120, 150); PINK2 = (196, 90, 122)
    d.polygon(S([(40, 600), (80, 440), (160, 400), (280, 400), (360, 440), (400, 600)]), fill=PINK)
    d.polygon(S([(160, 400), (280, 400), (250, 480), (190, 480)]), fill=SKIN)  # decote
    for x in range(90, 380, 40):
        d.ellipse(S((x, 560, x + 30, 590)), fill=PINK2)
    d.line(S([(160, 470), (280, 470)]), fill=(250, 247, 238), width=S(8))  # renda
    d.rectangle(S((195, 340, 245, 410)), fill=SKIN)
    d.ellipse(S((140, 200, 300, 380)), fill=SKIN)
    # penteado alto
    d.ellipse(S((120, 40, 320, 270)), fill=WIG)
    for (x, y) in [(118, 250), (300, 250), (116, 300), (302, 300)]:
        d.ellipse(S((x - 22, y - 22, x + 22, y + 22)), fill=WIG)
    d.ellipse(S((150, 150, 290, 250)), fill=SKIN)
    d.rectangle(S((150, 200, 290, 250)), fill=SKIN)
    d.ellipse(S((250, 60, 300, 110)), fill=PINK2)  # laço no cabelo
    # rosto
    d.ellipse(S((180, 262, 196, 278)), fill=INK); d.ellipse(S((244, 262, 260, 278)), fill=INK)
    d.ellipse(S((166, 296, 192, 314)), fill=(240, 150, 150)); d.ellipse(S((248, 296, 274, 314)), fill=(240, 150, 150))
    d.ellipse(S((206, 318, 234, 334)), fill=(196, 50, 60))
    d.ellipse(S((262, 288, 270, 296)), fill=INK)  # pinta
    finish(im, 'dama', 'objetos')


buque(); marco(); palheta(); livro(); pergaminho(); dama()
registrar(['buque', 'marco', 'palheta', 'livro', 'pergaminho', 'dama'], 'objetos', 'CONTRABANDO')
