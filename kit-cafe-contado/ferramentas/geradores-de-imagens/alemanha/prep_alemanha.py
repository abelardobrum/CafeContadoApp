"""Peças novas do episódio A Alemanha toma o café brasileiro? (Café Contado) — desenhadas em código (MIT)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar, INK, CREAM


def wave_band(d, x0, x1, y0, y1, col, amp=14):
    top = [(x, y0 + math.sin((x - x0) / 60) * amp) for x in range(x0, x1 + 1, 6)]
    bot = [(x, y1 + math.sin((x - x0) / 60) * amp) for x in range(x1, x0 - 1, -6)]
    d.polygon(S(top + bot), fill=col)


def flag_de():
    """bandeira da Alemanha tremulando no mastro"""
    im, d = canvas(520, 440)
    d.rectangle(S((30, 20, 46, 430)), fill=(120, 96, 70)); d.ellipse(S((24, 10, 52, 38)), fill=(210, 170, 60))
    x0, x1 = 46, 490
    wave_band(d, x0, x1, 50, 140, (28, 24, 20))
    wave_band(d, x0, x1, 140, 230, (210, 32, 28))
    wave_band(d, x0, x1, 230, 320, (246, 196, 40))
    finish(im, 'flag_de', 'objetos')


def flag_us():
    """bandeira dos EUA tremulando no mastro"""
    im, d = canvas(520, 440)
    d.rectangle(S((30, 20, 46, 430)), fill=(120, 96, 70)); d.ellipse(S((24, 10, 52, 38)), fill=(210, 170, 60))
    x0, x1 = 46, 490
    h = 270 / 13
    for i in range(13):
        wave_band(d, x0, x1, int(50 + i * h), int(50 + (i + 1) * h) + 1, (200, 30, 40) if i % 2 == 0 else (245, 240, 232))
    pts = [(x, 50 + math.sin((x - x0) / 60) * 14) for x in range(x0, 250, 6)]
    pts += [(x, 50 + 7 * h + math.sin((x - x0) / 60) * 14) for x in range(246, x0 - 1, -6)]
    d.polygon(S(pts), fill=(40, 52, 120))
    for r in range(4):
        for c in range(6):
            x = 66 + c * 30 + (15 if r % 2 else 0); y = 70 + r * 32 + math.sin((x - x0) / 60) * 14
            d.ellipse(S((x - 5, y - 5, x + 5, y + 5)), fill=(245, 240, 232))
    finish(im, 'flag_us', 'objetos')


def pack_eu():
    """pacote de café torrado com marca europeia fictícia"""
    im, d = canvas(380, 520)
    d.polygon(S([(60, 70), (320, 70), (340, 500), (40, 500)]), fill=(48, 40, 34))
    d.polygon(S([(60, 70), (320, 70), (300, 30), (80, 30)]), fill=(70, 60, 50))
    for x in range(90, 300, 18):
        d.line(S([(x, 34), (x, 66)]), fill=(90, 78, 66), width=S(3))
    d.rounded_rectangle(S((80, 150, 300, 400)), radius=S(16), fill=CREAM)
    d.rectangle(S((80, 170, 300, 196)), fill=(28, 24, 20)); d.rectangle(S((80, 196, 300, 222)), fill=(210, 32, 28)); d.rectangle(S((80, 222, 300, 248)), fill=(246, 196, 40))
    d.ellipse(S((150, 268, 230, 340)), fill=(104, 64, 34)); d.arc(S((168, 272, 212, 336)), 250, 110, fill=CREAM, width=S(5))
    for i, w in enumerate((150, 110)):
        d.rounded_rectangle(S((190 - w // 2, 352 + i * 22, 190 + w // 2, 364 + i * 22)), radius=S(5), fill=(150, 130, 110))
    d.rectangle(S((40, 470, 340, 500)), fill=(70, 60, 50))
    finish(im, 'pack_eu', 'objetos')


def beans_green():
    """punhado de grãos de café verdes (crus)"""
    im, d = canvas(480, 340)
    pos = [(110, 200, 20), (200, 160, -30), (290, 210, 40), (380, 170, -10), (160, 260, 70), (260, 280, -50), (350, 270, 15), (220, 90, 60), (320, 110, -40), (130, 120, 10)]
    for x, y, a in pos:
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        pts = []
        for k in range(36):
            t = k / 36 * 2 * math.pi; ex, ey = 56 * math.cos(t), 40 * math.sin(t)
            pts.append((x + ex * ca - ey * sa, y + ex * sa + ey * ca))
        d.polygon(S([(px + 5, py + 6) for px, py in pts]), fill=(60, 70, 40))
        d.polygon(S(pts), fill=(150, 168, 98))
        line = [(x + u * ca + math.sin(u / 12) * 6 * -sa, y + u * sa + math.sin(u / 12) * 6 * ca) for u in range(-44, 45, 4)]
        d.line(S(line), fill=(96, 112, 58), width=S(5))
    finish(im, 'beans_green', 'objetos')


flag_de(); flag_us(); pack_eu(); beans_green()
registrar(['flag_de', 'flag_us', 'pack_eu', 'beans_green'], 'objetos', 'ALEMANHA')
