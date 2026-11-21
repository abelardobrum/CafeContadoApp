"""Peças novas do episódio Café emagrece? (Café Contado) — desenhadas em código (MIT).
Saem em biblioteca/objetos/*.png. Reusa tone/finish do gerador arabica-robusta."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM


def bathscale():
    """balança de banheiro com mostrador"""
    im, d = canvas(460, 440)
    d.rounded_rectangle(S((30, 40, 430, 420)), radius=S(60), fill=(206, 206, 200))
    d.rounded_rectangle(S((50, 60, 410, 400)), radius=S(48), fill=(232, 230, 222))
    d.rounded_rectangle(S((120, 90, 340, 200)), radius=S(20), fill=INK)
    d.rounded_rectangle(S((134, 104, 326, 186)), radius=S(14), fill=CREAM)
    for i in range(9):
        x = 150 + i * 20
        d.line(S([(x, 110), (x, 126 if i % 2 else 138)]), fill=INK, width=S(3))
    d.line(S([(230, 182), (262, 118)]), fill=(200, 30, 30), width=S(6))
    for x0 in (90, 260):  # pés / pegadas
        d.ellipse(S((x0, 240, x0 + 110, 380)), fill=(180, 178, 170))
        d.ellipse(S((x0 + 15, 255, x0 + 95, 365)), fill=(196, 194, 186))
    finish(im, 'bathscale', 'objetos')


def sugar():
    """colher com açúcar + dois cubos"""
    im, d = canvas(520, 380)
    d.line(S([(60, 330), (300, 190)]), fill=(150, 150, 156), width=S(26))
    d.ellipse(S((270, 110, 470, 250)), fill=(150, 150, 156))
    d.ellipse(S((285, 122, 455, 238)), fill=(196, 196, 202))
    for i in range(60):  # montinho de açúcar
        a = i * 2.399; r = 60 * math.sqrt(i / 60)
        x, y = 370 + math.cos(a) * r, 175 + math.sin(a) * r * 0.55 - 14
        d.rectangle(S((x - 5, y - 5, x + 5, y + 5)), fill=(252, 252, 248))
    for (x, y, rot) in [(90, 120, 0), (190, 70, 0)]:
        d.polygon(S([(x, y + 30), (x + 70, y), (x + 140, y + 30), (x + 70, y + 60)]), fill=(255, 255, 252))
        d.polygon(S([(x, y + 30), (x + 70, y + 60), (x + 70, y + 140), (x, y + 110)]), fill=(222, 222, 216))
        d.polygon(S([(x + 70, y + 60), (x + 140, y + 30), (x + 140, y + 110), (x + 70, y + 140)]), fill=(238, 238, 232))
    finish(im, 'sugar', 'objetos')


def bolt():
    """raio de energia (adrenalina)"""
    im, d = canvas(300, 460)
    pts = [(170, 20), (50, 250), (150, 250), (100, 440), (260, 180), (160, 180), (230, 20)]
    d.polygon(S([(x + 8, y + 8) for x, y in pts]), fill=INK)
    d.polygon(S(pts), fill=(246, 196, 40))
    d.polygon(S([(180, 40), (90, 230), (120, 230)]), fill=(255, 232, 140))
    finish(im, 'bolt', 'objetos')


bathscale(); sugar(); bolt()
registrar(['bathscale', 'sugar', 'bolt'], 'objetos', 'CAFE-EMAGRECE')
