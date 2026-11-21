"""Reconstrói biblioteca/indice.json e o catalogo.html a partir das pastas da biblioteca.

Para acrescentar uma imagem nova: salve o PNG na pasta da categoria certa em biblioteca/
(nomes sem espaço nem acento, ex.: bg_porto.png, xicara_azul.png) e rode:
  python ferramentas/gerar_catalogo.py
"""
import os, json, html
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(KIT, 'biblioteca')
IMG_DIRS = ['cenarios', 'papeis-de-fundo', 'personagens', 'objetos', 'lavoura-e-clima', 'mapas', 'recortes-de-jornal', 'marca', 'extras-estilo-original']
TIT = {'cenarios': 'Cenários (fundos de tela cheia)', 'papeis-de-fundo': 'Papéis de fundo das cenas', 'personagens': 'Personagens (bonecos)',
       'objetos': 'Objetos e figuras', 'lavoura-e-clima': 'Lavoura, plantas e clima', 'mapas': 'Mapas', 'recortes-de-jornal': 'Recortes de jornal e mão',
       'marca': 'Marca Coffee Hub', 'extras-estilo-original': 'Extras do estilo original (não usados ainda)'}
old = json.load(open(os.path.join(B, 'indice.json'), encoding='utf-8')) if os.path.exists(os.path.join(B, 'indice.json')) else {}
idx = {}
for c in IMG_DIRS:
    d = os.path.join(B, c)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            if f in idx: print('AVISO: nome repetido', f, '— renomeie um deles')
            e = dict(old.get(f, {})); e.update(categoria=c, caminho=f'biblioteca/{c}/{f}')
            idx[f] = e
idx['layout.json'] = {'categoria': 'personagens', 'caminho': 'biblioteca/personagens/layout.json'}
json.dump(idx, open(os.path.join(B, 'indice.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

def nome(f, e):
    n = os.path.splitext(f)[0]
    if e['categoria'] == 'personagens':
        if n.endswith('_face'): return "who: '" + {'lurdes': 'l', 'neto': 'n'}.get(n[:-5], n[:-5]) + "'"
        return None
    return e.get('nome_no_codigo') or n
sec = []
for c in IMG_DIRS:
    items = [(f, e) for f, e in idx.items() if e['categoria'] == c and f != 'layout.json']
    if c == 'personagens': items = [(f, e) for f, e in items if f.endswith('_face.png') or f == 'p_face.png']
    if not items: continue
    cards = ''.join(
        f'<figure data-n="{html.escape(f.lower())}"><div class="im{" bg" if c in ("cenarios","papeis-de-fundo") else ""}"><img loading="lazy" src="{html.escape(e["caminho"])}"></div>'
        f'<figcaption><b>{html.escape(nome(f, e) or f)}</b><span>{html.escape(f)}</span>'
        f'{"<i>" + html.escape(e["criado_em"]) + "</i>" if e.get("criado_em") else ""}</figcaption></figure>' for f, e in items)
    sec.append(f'<h2>{TIT[c]} <small>{len(items)}</small></h2><div class="grid">{cards}</div>')
musicas = sorted(f for f in os.listdir(os.path.join(B, 'musicas')) if f.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg'))) if os.path.isdir(os.path.join(B, 'musicas')) else []
sfx = sorted(f for f in os.listdir(os.path.join(B, 'efeitos-sonoros')) if f.lower().endswith(('.mp3', '.wav', '.flac', '.ogg'))) if os.path.isdir(os.path.join(B, 'efeitos-sonoros')) else []
au = ''.join(f'<div class="au"><span>{html.escape(m)}</span><audio controls preload="none" src="biblioteca/musicas/{html.escape(m)}"></audio></div>' for m in musicas)
au += ''.join(f'<div class="au"><span>{html.escape(m)}</span><audio controls preload="none" src="biblioteca/efeitos-sonoros/{html.escape(m)}"></audio></div>' for m in sfx)
page = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Catálogo · Kit de colagem animada</title>
<style>
body{{margin:0;background:#efe6d3;font:15px/1.4 system-ui,sans-serif;color:#2a2018}}
header{{position:sticky;top:0;background:#0c3529;color:#f4ecd8;padding:14px 24px;display:flex;gap:20px;align-items:center;z-index:2}}
header h1{{margin:0;font-size:20px}} header input{{flex:1;max-width:360px;padding:8px 12px;border-radius:6px;border:0;font-size:15px}}
main{{padding:8px 24px 60px}} h2{{margin:28px 0 10px;border-bottom:2px solid #c99e41;padding-bottom:4px}} h2 small{{color:#8a7a60;font-weight:400}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
figure{{margin:0;background:#fffaf0;border-radius:8px;padding:8px;box-shadow:0 1px 3px #0002}}
.im{{height:130px;display:flex;align-items:center;justify-content:center;background:repeating-conic-gradient(#e7dfcf 0 25%,#f6f0e4 0 50%) 0/16px 16px;border-radius:4px}}
.im.bg{{height:220px}} .im img{{max-width:100%;max-height:100%}}
figcaption{{margin-top:6px;display:flex;flex-direction:column;font-size:12px}} figcaption b{{font-size:13px;color:#0c3529;word-break:break-all}}
figcaption span{{color:#6a5c48;word-break:break-all}} figcaption i{{color:#a08a68}}
.au{{display:flex;align-items:center;gap:12px;margin:6px 0}} .au span{{min-width:340px}}
p.dica{{background:#fffaf0;padding:10px 14px;border-left:4px solid #c99e41}}
</style></head><body>
<header><h1>Kit de colagem animada · catálogo</h1><input id="q" placeholder="buscar (ex.: bg_, saco, mapa)…"><span>{len(idx)-1} imagens</span></header>
<main>
<p class="dica">Em negrito: o nome usado no código da cena (<code>img: 'nome'</code>; para personagens, <code>k: 'lurdes', who: 'nome'</code>).
Embaixo: o arquivo e o episódio em que a peça foi criada. Para usar uma peça nova num episódio, acrescente no index.html:
<code>srcs['nome'] = '/biblioteca/_/arquivo.png';</code></p>
{''.join(sec)}
<h2>Músicas e efeitos sonoros</h2>{au}
</main>
<script>
q.oninput=()=>{{const v=q.value.toLowerCase();document.querySelectorAll('figure').forEach(f=>f.style.display=f.dataset.n.includes(v)||f.querySelector('b').textContent.toLowerCase().includes(v)?'':'none')}};
</script></body></html>'''
open(os.path.join(KIT, 'catalogo.html'), 'w', encoding='utf-8').write(page)
print('indice.json e catalogo.html atualizados:', len(idx) - 1, 'imagens')
