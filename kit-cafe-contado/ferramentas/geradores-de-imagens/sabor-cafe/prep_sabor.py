"""Peças novas do episódio "Sabor" Café (Café Contado) — pacotes de café desenhados em código (MIT)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM
from PIL import ImageFont

FB = 'C:/Windows/Fonts/arialbd.ttf'
def F(sz): return ImageFont.truetype(FB, S(sz))

def ctext(d, cx, y, txt, sz, fill):
    f = F(sz); w = d.textlength(txt, font=f)
    d.text((S(cx) - w / 2, S(y)), txt, font=f, fill=fill)

def pacote(nome, corpo, faixa, fino, fino_cor):
    im, d = canvas(380, 560)
    # sombra + corpo
    d.rounded_rectangle(S((38, 58, 358, 548)), radius=S(18), fill=INK)
    d.rounded_rectangle(S((28, 48, 348, 538)), radius=S(18), fill=corpo)
    # topo serrilhado (selagem)
    d.rectangle(S((28, 30, 348, 70)), fill=tuple(max(0, c - 30) for c in corpo))
    for x in range(28, 348, 16):
        d.polygon(S([(x, 30), (x + 8, 18), (x + 16, 30)]), fill=tuple(max(0, c - 30) for c in corpo))
    for x in range(40, 340, 12):
        d.line(S([(x, 38), (x, 62)]), fill=tuple(max(0, c - 55) for c in corpo), width=S(2))
    # brilho lateral
    d.rectangle(S((44, 80, 58, 520)), fill=tuple(min(255, c + 35) for c in corpo))
    # rótulo
    d.rounded_rectangle(S((70, 110, 306, 450)), radius=S(14), fill=CREAM)
    d.rectangle(S((70, 140, 306, 178)), fill=faixa)
    ctext(d, 188, 145, 'TRADICIONAL', 26, CREAM)
    ctext(d, 188, 192, 'CAFÉ', 64, INK)
    # xícara
    d.ellipse(S((120, 345, 256, 375)), fill=(200, 196, 186))
    d.chord(S((132, 260, 244, 368)), 0, 180, fill=(250, 248, 240), outline=INK, width=S(3))
    d.ellipse(S((132, 300, 244, 322)), fill=(250, 248, 240), outline=INK, width=S(3))
    d.ellipse(S((140, 303, 236, 319)), fill=(92, 52, 26))
    d.arc(S((228, 312, 268, 348)), 270, 90, fill=INK, width=S(5))
    for x in (160, 188, 216):
        d.arc(S((x - 10, 250, x + 10, 290)), 100, 260, fill=(140, 120, 100), width=S(3))
    # letra miúda
    ctext(d, 188, 392, fino, 13, fino_cor)
    ctext(d, 188, 412, '500 g', 18, INK)
    finish(im, nome, 'objetos')

pacote('pacote_cafe', (150, 40, 34), (60, 120, 60), 'CAFÉ TORRADO E MOÍDO', INK)
pacote('pacote_sabor', (150, 40, 34), (60, 120, 60), 'PÓ P/ BEBIDA SABOR CAFÉ', (120, 110, 100))
registrar(['pacote_cafe', 'pacote_sabor'], 'objetos', 'SABOR-CAFE')
