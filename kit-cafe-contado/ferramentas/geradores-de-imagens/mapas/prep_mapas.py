"""Mapas no estilo simples do worldmap (polígonos chapados, grade, kraft), a partir do Natural Earth (domínio público).
Uso: python3 prep_mapas.py land50m.geojson [--registrar]  -> biblioteca/mapas/{mapa_europa,mapa_asia,mapa_mundo}.png (MIT)"""
import os, sys, json, math
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pecas import canvas, S, finish, registrar

OCEAN = (187, 211, 214); GRID = (150, 182, 190); LAND = (206, 181, 133); FRAME = (243, 236, 220)
GEO = json.load(open(sys.argv[1], encoding='utf-8'))
geom = GEO['features'][0]['geometry'] if 'features' in GEO else GEO['geometry']
POLYS = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]

def dp(pts, eps):  # Douglas-Peucker
    if len(pts) < 3: return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1e-9
    i, dmax = 0, -1
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + x1 * y0 - y1 * x0) / L
        if d > dmax: i, dmax = k, d
    if dmax <= eps: return [pts[0], pts[-1]]
    return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)

def area(p):
    return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2

def build(name, lon0, lon1, lat0, lat1, W, eps=9, min_area=900, step=100):
    c = math.cos(math.radians((lat0 + lat1) / 2)) if name != 'mapa_mundo' else 1.0
    k = (W - 36) / ((lon1 - lon0) * c); H = int((lat1 - lat0) * k) + 36
    P = lambda lo, la: (18 + (lo - lon0) * c * k, 18 + (lat1 - la) * k)
    im, d = canvas(W, H)
    d.rectangle(S((18, 18, W - 18, H - 18)), fill=OCEAN)
    for x in range(18 + step // 2, W - 18, step): d.line(S([(x, 18), (x, H - 18)]), fill=GRID, width=S(2))
    for y in range(18 + step // 2, H - 18, step): d.line(S([(18, y), (W - 18, y)]), fill=GRID, width=S(2))
    for poly in POLYS:
        for ri, ring0 in enumerate(poly):
            ring = [list(ring0[0])]
            for lo, la in ring0[1:]:  # desfaz o salto no antimeridiano
                while lo - ring[-1][0] > 180: lo -= 360
                while lo - ring[-1][0] < -180: lo += 360
                ring.append([lo, la])
            shifts = [0] + ([-360] if max(r[0] for r in ring) > 180 else []) + ([360] if min(r[0] for r in ring) < -180 else [])
            for sh in shifts:
                pts = [P(lo + sh, la) for lo, la in ring]
                if area(pts) < min_area: continue
                h = len(pts) // 2
                sp = dp(pts[:h + 1], eps)[:-1] + dp(pts[h:], eps)
                if len(sp) >= 3: d.polygon(S(sp), fill=LAND if ri == 0 else OCEAN)
    fr = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(fr).rectangle(S((0, 0, W, H)), fill=FRAME)
    hole = Image.new('L', im.size, 255); ImageDraw.Draw(hole).rectangle(S((18, 18, W - 18, H - 18)), fill=0)
    fr.putalpha(hole); im.alpha_composite(fr)
    finish(im, name, 'mapas')
    return P, W, H

PLACES = {
 'Brasil': (-51, -10), 'EUA': (-98, 39), 'México': (-102, 23), 'Colômbia': (-73, 4), 'Portugal': (-8.2, 39.6),
 'Espanha': (-3.7, 40.3), 'França': (2.5, 46.5), 'Reino Unido': (-2, 53), 'Bélgica': (4.6, 50.6), 'Holanda': (5.6, 52.3),
 'Alemanha': (10.4, 51), 'Suíça': (8.2, 46.8), 'Itália': (12.5, 42.8), 'Polônia': (19.4, 52), 'Suécia': (16, 62.5),
 'Noruega': (9, 61.5), 'Finlândia': (26, 63), 'Grécia': (22, 39.5), 'Ucrânia': (31, 49), 'Turquia': (35, 39),
 'Rússia': (45, 57), 'Marrocos': (-6, 32), 'Argélia': (3, 28), 'Egito': (30, 26.5), 'Etiópia': (39.5, 8.6),
 'Arábia Saudita': (45, 24), 'Dubai': (55.3, 25.2), 'Irã': (53, 32), 'Índia': (79, 22), 'China': (104, 35),
 'Mongólia': (103, 47), 'Coreia do Sul': (127.8, 36.4), 'Japão': (138.5, 36.5), 'Vietnã': (106.3, 15.5),
 'Tailândia': (101, 15), 'Filipinas': (122, 12), 'Indonésia': (117, -2), 'Austrália': (134, -25),
 'Nova Zelândia': (172, -41), 'África do Sul': (24, -29), 'Quênia': (37.9, 0.2), 'Canadá': (-106, 58),
}
lines = []
def coords(name, P, W, H):
    row = []
    for nm, (lo, la) in PLACES.items():
        x, y = P(lo, la)
        if 40 < x < W - 40 and 40 < y < H - 40:
            if name == 'mapa_asia' and nm == 'Rússia': continue
            row.append(f'{nm} ({round(540 + x - W / 2)},{round(900 + y - H / 2)})')
    lines.append(f'{name}: ' + ' · '.join(row))

for args in [('mapa_europa', -22, 64, 8, 72, 1020), ('mapa_asia', 58, 180, -48, 58, 1020), ('mapa_mundo', -170, 190, -56, 78, 1020)]:
    P, W, H = build(*args, eps=9 if args[0] != 'mapa_mundo' else 4, min_area=900 if args[0] != 'mapa_mundo' else 120)
    coords(args[0], P, W, H)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapas_coords.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
if '--registrar' in sys.argv: registrar(['mapa_europa', 'mapa_asia', 'mapa_mundo'], 'mapas', 'MAPAS-2026-11')
