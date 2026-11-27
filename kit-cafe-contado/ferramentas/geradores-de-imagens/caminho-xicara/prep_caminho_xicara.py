"""Peças novas do episódio O Caminho da Xícara (Café Contado) — desenhadas em código (MIT).
caminhao (truck com sacas, de lado, virado p/ direita), conteiner, guindaste (porto)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

RED = (196, 40, 32); RED_D = (150, 28, 24)
JUTA = (196, 160, 104); JUTA_D = (160, 124, 76)
GRAY = (70, 70, 74); GLASS = (150, 190, 205)


def roda(d, cx, cy, r=46):
    d.ellipse(S((cx - r, cy - r, cx + r, cy + r)), fill=INK)
    d.ellipse(S((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55)), fill=(170, 170, 172))
    d.ellipse(S((cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2)), fill=GRAY)


def caminhao():
    """caminhão de carroceria aberta carregado de sacas de café, virado para a direita"""
    im, d = canvas(720, 400)
    # carroceria
    d.rectangle(S((30, 230, 500, 300)), fill=(120, 78, 44))
    d.rectangle(S((30, 230, 500, 244)), fill=(150, 100, 58))
    for x in range(60, 500, 60):
        d.line(S([(x, 244), (x, 300)]), fill=(96, 60, 32), width=S(4))
    # sacas empilhadas (3 fileiras)
    for row, (y, n, off) in enumerate([(170, 5, 0), (112, 4, 46), (56, 3, 92)]):
        for i in range(n):
            x = 44 + off + i * 92
            d.rounded_rectangle(S((x, y, x + 92, y + 64)), radius=S(22), fill=JUTA_D)
            d.rounded_rectangle(S((x + 4, y + 2, x + 88, y + 58)), radius=S(20), fill=JUTA)
            d.line(S([(x + 20, y + 30), (x + 72, y + 30)]), fill=RED_D, width=S(4))
            d.text(S((x + 36, y + 10)), 'BR', fill=RED_D)
    # chassi
    d.rectangle(S((30, 300, 690, 322)), fill=GRAY)
    # cabine
    d.polygon(S([(520, 300), (520, 120), (620, 120), (680, 200), (690, 210), (690, 300)]), fill=RED)
    d.polygon(S([(540, 140), (612, 140), (660, 200), (540, 200)]), fill=GLASS)
    d.line(S([(560, 150), (600, 190)]), fill=(220, 240, 245), width=S(6))
    d.rectangle(S((520, 120, 530, 300)), fill=RED_D)
    d.line(S([(540, 214), (540, 290)]), fill=RED_D, width=S(4))
    d.rectangle(S((552, 226, 584, 236)), fill=INK)
    d.rectangle(S((672, 240, 698, 300)), fill=(225, 225, 220))  # para-choque/grade
    for y in range(248, 296, 12):
        d.line(S([(676, y), (694, y)]), fill=GRAY, width=S(3))
    d.ellipse(S((680, 214, 698, 232)), fill=(250, 220, 90))  # farol
    d.rectangle(S((500, 60, 512, 300)), fill=GRAY)  # escapamento
    # rodas
    for cx in (110, 220, 610):
        roda(d, cx, 330)
    finish(im, 'caminhao', 'objetos')


def conteiner():
    """contêiner marítimo vermelho"""
    im, d = canvas(560, 300)
    d.rectangle(S((20, 30, 540, 280)), fill=RED_D)
    d.rectangle(S((30, 40, 530, 270)), fill=RED)
    for x in range(48, 530, 26):
        d.rectangle(S((x, 46, x + 12, 264)), fill=RED_D)
    d.rectangle(S((20, 30, 540, 44)), fill=(120, 22, 20))
    d.rectangle(S((20, 266, 540, 280)), fill=(120, 22, 20))
    for x in (20, 524):
        d.rectangle(S((x, 30, x + 16, 280)), fill=(110, 20, 18))
    d.rectangle(S((190, 120, 370, 190)), fill=CREAM)
    d.text(S((214, 140)), 'COFFEE  BR', fill=INK)
    finish(im, 'conteiner', 'objetos')


def guindaste():
    """guindaste de porto (pórtico) com contêiner pendurado"""
    im, d = canvas(520, 640)
    Y = (240, 184, 40); Y_D = (190, 140, 24)
    # pernas
    for x in (110, 300):
        d.polygon(S([(x, 620), (x + 30, 620), (x + 30, 200), (x, 200)]), fill=Y)
        d.line(S([(x + 15, 210), (x + 15, 610)]), fill=Y_D, width=S(4))
    for y in (300, 420, 540):
        d.line(S([(140, y), (300, y + 60)]), fill=Y_D, width=S(8))
        d.line(S([(300, y), (140, y + 60)]), fill=Y_D, width=S(8))
    # lança horizontal
    d.rectangle(S((20, 160, 510, 200)), fill=Y)
    for x in range(30, 500, 40):
        d.line(S([(x, 162), (x + 40, 198)]), fill=Y_D, width=S(4))
    d.polygon(S([(180, 160), (260, 40), (290, 40), (290, 160)]), fill=Y)
    d.line(S([(275, 46), (40, 162)]), fill=INK, width=S(4))
    d.line(S([(275, 46), (500, 162)]), fill=INK, width=S(4))
    d.rectangle(S((200, 210, 290, 260)), fill=(225, 225, 220))  # cabine
    d.rectangle(S((210, 218, 280, 244)), fill=GLASS)
    # cabo + contêiner
    d.line(S([(440, 200), (440, 330)]), fill=INK, width=S(4))
    d.rectangle(S((370, 330, 510, 400)), fill=(40, 96, 150))
    for x in range(380, 505, 16):
        d.rectangle(S((x, 336, x + 7, 394)), fill=(28, 70, 116))
    # base trilhos
    d.rectangle(S((90, 620, 350, 636)), fill=GRAY)
    finish(im, 'guindaste', 'objetos')


caminhao(); conteiner(); guindaste()
registrar(['caminhao', 'conteiner', 'guindaste'], 'objetos', 'O-CAMINHO-DA-XICARA')
