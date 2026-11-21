"""Peças novas do episódio Qual café o Jason bebe? (Café Contado) — desenhadas em código."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM

def wave(d, x0, y0, w, h, rows, cols_fn):
    # bandeira levemente ondulada: faixas horizontais em polígonos
    n = 24
    for r in range(rows):
        top = y0 + h * r / rows; bot = y0 + h * (r + 1) / rows
        for i in range(n):
            xa = x0 + w * i / n; xb = x0 + w * (i + 1) / n
            oa = math.sin(i / n * math.pi * 2) * 14; ob = math.sin((i + 1) / n * math.pi * 2) * 14
            d.polygon(S([(xa, top + oa), (xb, top + ob), (xb, bot + ob), (xa, bot + oa)]), fill=cols_fn(r, xa, top))

def pole(d, x, y0, y1):
    d.rectangle(S((x - 10, y0, x + 10, y1)), fill=(120, 110, 100))
    d.ellipse(S((x - 18, y0 - 30, x + 18, y0 + 6)), fill=(222, 180, 60))

def flag_us():
    im, d = canvas(620, 520)
    pole(d, 50, 40, 500)
    RED, WH, BL = (196, 32, 40), (246, 244, 236), (34, 52, 120)
    wave(d, 60, 60, 520, 330, 13, lambda r, x, y: RED if r % 2 == 0 else WH)
    n = 24
    for i in range(int(n * 0.42)):
        xa = 60 + 520 * i / n; xb = 60 + 520 * (i + 1) / n
        oa = math.sin(i / n * math.pi * 2) * 14; ob = math.sin((i + 1) / n * math.pi * 2) * 14
        d.polygon(S([(xa, 60 + oa), (xb, 60 + ob), (xb, 238 + ob), (xa, 238 + oa)]), fill=BL)
    for r in range(5):
        for c in range(6):
            x = 76 + c * 34 + (17 if r % 2 else 0); y = 82 + r * 32 + math.sin((x - 60) / 520 * math.pi * 2) * 14
            if x < 270: d.ellipse(S((x - 6, y - 6, x + 6, y + 6)), fill=WH)
    finish(im, 'flag_us', 'objetos')

def flag_de():
    im, d = canvas(620, 520)
    pole(d, 50, 40, 500)
    cols = [(24, 22, 22), (204, 30, 34), (250, 200, 30)]
    wave(d, 60, 60, 520, 330, 3, lambda r, x, y: cols[r])
    finish(im, 'flag_de', 'objetos')

def flag_br():
    im, d = canvas(620, 520)
    pole(d, 50, 40, 500)
    wave(d, 60, 60, 520, 330, 1, lambda r, x, y: (20, 140, 70))
    d.polygon(S([(320, 95), (540, 225), (320, 355), (100, 225)]), fill=(250, 210, 30))
    d.ellipse(S((240, 145, 400, 305)), fill=(30, 50, 130))
    d.arc(S((200, 175, 440, 375)), 225, 315, fill=(246, 244, 236), width=S(12))
    finish(im, 'flag_br', 'objetos')

def gamepad():
    im, d = canvas(560, 360)
    d.rounded_rectangle(S((40, 70, 520, 250)), radius=S(80), fill=(40, 40, 46))
    d.ellipse(S((30, 120, 220, 330)), fill=(40, 40, 46)); d.ellipse(S((340, 120, 530, 330)), fill=(40, 40, 46))
    d.rectangle(S((110, 135, 140, 215)), fill=(150, 150, 160)); d.rectangle(S((85, 160, 165, 190)), fill=(150, 150, 160))
    for (x, y, c) in [(410, 120, (60, 190, 90)), (450, 160, (220, 60, 60)), (370, 160, (60, 120, 220)), (410, 200, (240, 200, 40))]:
        d.ellipse(S((x - 18, y - 18, x + 18, y + 18)), fill=c)
    d.ellipse(S((200, 200, 260, 260)), fill=(90, 90, 100)); d.ellipse(S((300, 200, 360, 260)), fill=(90, 90, 100))
    finish(im, 'gamepad', 'objetos')

def graph(name, up):
    im, d = canvas(520, 440)
    d.rectangle(S((40, 30, 480, 410)), fill=(246, 242, 228))
    for y in range(80, 400, 60): d.line(S([(40, y), (480, y)]), fill=(210, 204, 186), width=S(2))
    d.line(S([(60, 40), (60, 390), (470, 390)]), fill=INK, width=S(6))
    pts = [(80, 120), (170, 150), (250, 130), (330, 300), (440, 350)] if not up else [(80, 330), (170, 300), (250, 310), (330, 180), (440, 80)]
    col = (200, 30, 40) if not up else (30, 150, 70)
    d.line(S(pts), fill=col, width=S(14), joint='curve')
    x, y = pts[-1]; px, py = pts[-2]
    a = math.atan2(y - py, x - px)
    tip = [(x + math.cos(a) * 30, y + math.sin(a) * 30), (x + math.cos(a + 2.4) * 34, y + math.sin(a + 2.4) * 34), (x + math.cos(a - 2.4) * 34, y + math.sin(a - 2.4) * 34)]
    d.polygon(S(tip), fill=col)
    finish(im, name, 'objetos')

flag_us(); flag_de(); flag_br(); gamepad(); graph('graf_queda', False); graph('graf_alta', True)
registrar(['flag_us', 'flag_de', 'flag_br', 'gamepad', 'graf_queda', 'graf_alta'], 'objetos', 'QUAL-CAFE-JASON')
