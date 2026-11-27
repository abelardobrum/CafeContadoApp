import sys, os
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(KIT, 'ferramentas', 'geradores-de-imagens'))
from pecas import canvas, S, finish, registrar, INK, CREAM

BROWN = (92, 54, 30); DARK = (52, 30, 18); PAPER = (240, 232, 214); PAPER2 = (222, 210, 186)
RED = (190, 40, 36); STEEL = (168, 172, 176); STEEL2 = (120, 124, 130); GLASS = (200, 222, 230)
CREMA = (196, 140, 80)

# --- coador: suporte de papel (cone) sobre um bule de vidro ---
im, d = canvas(420, 520)
# bule de vidro
d.rounded_rectangle(S((70, 250, 330, 500)), radius=S(30), fill=GLASS, outline=INK, width=S(6))
d.rounded_rectangle(S((80, 330, 320, 490)), radius=S(24), fill=DARK)
d.rectangle(S((80, 330, 320, 345)), fill=BROWN)
d.arc(S((300, 290, 390, 440)), -90, 90, fill=INK, width=S(14))
d.line(S([(110, 270), (110, 470)]), fill=(255, 255, 255), width=S(6))
# cone (suporte vermelho)
d.polygon(S([(30, 40), (370, 40), (260, 240), (140, 240)]), fill=RED, outline=INK)
d.line(S([(30, 40), (370, 40), (260, 240), (140, 240), (30, 40)]), fill=INK, width=S(6))
d.rectangle(S((120, 236, 280, 262)), fill=RED, outline=INK, width=S(5))
# papel dobrado aparecendo
d.polygon(S([(55, 10), (345, 10), (322, 52), (78, 52)]), fill=PAPER, outline=INK)
for x in (110, 170, 230, 290):
    d.line(S([(x, 14), (x - 4, 50)]), fill=PAPER2, width=S(3))
# pó dentro
d.ellipse(S((90, 20, 310, 50)), fill=BROWN)
# gotas
for y in (272, 300):
    d.ellipse(S((193, y, 207, y + 18)), fill=DARK)
finish(im, 'coador', 'objetos')

# --- máquina de expresso ---
im, d = canvas(480, 520)
d.rounded_rectangle(S((20, 20, 460, 130)), radius=S(16), fill=STEEL, outline=INK, width=S(6))
d.rectangle(S((40, 40, 440, 60)), fill=STEEL2)
d.ellipse(S((360, 70, 400, 110)), fill=RED, outline=INK, width=S(4))
d.ellipse(S((300, 75, 330, 105)), fill=(250, 250, 250), outline=INK, width=S(4))
d.rectangle(S((40, 130, 120, 470)), fill=STEEL, outline=INK, width=S(6))
d.rectangle(S((360, 130, 440, 470)), fill=STEEL, outline=INK, width=S(6))
d.rectangle(S((20, 460, 460, 505)), fill=STEEL2, outline=INK, width=S(6))
# grupo + porta-filtro
d.rectangle(S((190, 130, 290, 170)), fill=STEEL2, outline=INK, width=S(5))
d.rounded_rectangle(S((170, 165, 310, 205)), radius=S(10), fill=(60, 60, 64), outline=INK, width=S(5))
d.rounded_rectangle(S((300, 175, 430, 195)), radius=S(8), fill=INK)
d.rectangle(S((215, 205, 225, 222)), fill=INK); d.rectangle(S((255, 205, 265, 222)), fill=INK)
# fio de café
d.rectangle(S((218, 222, 223, 360)), fill=DARK); d.rectangle(S((258, 222, 263, 360)), fill=DARK)
# xicrinha
d.polygon(S([(180, 360), (300, 360), (285, 445), (195, 445)]), fill=(248, 244, 236), outline=INK)
d.line(S([(180, 360), (300, 360), (285, 445), (195, 445), (180, 360)]), fill=INK, width=S(5))
d.ellipse(S((184, 352, 296, 372)), fill=CREMA, outline=INK, width=S(3))
d.arc(S((280, 375, 325, 420)), -90, 90, fill=INK, width=S(8))
d.ellipse(S((165, 438, 315, 460)), fill=(248, 244, 236), outline=INK, width=S(4))
finish(im, 'maq_expresso', 'objetos')

# --- caneca grande ---
im, d = canvas(380, 400)
d.rounded_rectangle(S((40, 40, 280, 370)), radius=S(26), fill=RED, outline=INK, width=S(7))
d.arc(S((230, 110, 350, 280)), -90, 90, fill=INK, width=S(30))
d.arc(S((236, 116, 344, 274)), -90, 90, fill=RED, width=S(16))
d.ellipse(S((40, 22, 280, 70)), fill=DARK, outline=INK, width=S(7))
d.rectangle(S((70, 170, 250, 240)), fill=CREAM)
d.line(S([(68, 90), (68, 340)]), fill=(225, 90, 80), width=S(10))
finish(im, 'caneca', 'objetos')

registrar(['coador', 'maq_expresso', 'caneca'], 'objetos', 'CAFE-EXPRESSO-OU-NO-COADOR-QUAL-E-MAIS-FORTE')
