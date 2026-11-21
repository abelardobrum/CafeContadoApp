# CAFÉ CONTADO — guia rápido do kit (ler SÓ este arquivo)

Não ler: README.md, skills/, catalogo.html, biblioteca/indice.json, modelos/cafe-contado/index.html,
index.html de episódios antigos, _arquivo/. Tudo o que importa está aqui.

## Fluxo (VM Linux: `cd $HOME/mnt/StudioViraly/kit-cafe-contado`) — 3 comandos, sem reprocesso
1. Entrada (pedir tudo de uma vez): copy, título de tela, narração .mp3, música. **Selo**: o usuário escolhe no pedido (ex.: EP.5, CURIOSIDADE ou sem selo) — não há padrão; se não disser, perguntar. Destino final: `saida/<Selo> - <Título>` no próprio kit (ex.: "EP. 5 - Título", "Curiosidade - Título"; sem selo = só `saida/<Título>`). `episodios/cafe-contado/<EP>` é só pasta de trabalho (recriada sozinha; pode ser apagada após o render).
   Commit dos áudios + copy em `entrada/<slug>/` (narr.mp3, musica.mp3, copy.txt), nomes NOVOS em /mnt/user-data/outputs.
2. `python3 ferramentas/cc.py novo <EP> --narracao entrada/<slug>/narr.mp3 --copy entrada/<slug>/copy.txt --musica entrada/<slug>/musica.mp3`
   → checa/instala dependências, copia os áudios e imprime palavra@tempo + DUR.
3. Escrever `episodios/cafe-contado/<EP>/cenas.js` + `legenda.txt` com os ATALHOS e o esqueleto abaixo (não ler episódios antigos).
4. `cc.py previa <EP>` → valida (img sem PECAS, faixa da legenda, 5 hashtags + #CafeContado), monta, 1 quadro no fim de cada cena + capa
   em UMA imagem `out/contato.jpg` (~45 s). Olhar uma vez, juntar TODOS os ajustes.
5. (se preciso, 1 rodada) `cc.py ajustar <EP> trocas.txt` — linhas `ANTIGO ==> NOVO` (trecho único do cenas.js). Aplica as que casam,
   lista as puladas (corrigir só essas), monta e gera quadros SÓ das cenas alteradas (+ capa se mexeu nela).
6. `cc.py finalizar <EP> "Título"` → áudio (pula se já atualizado), capa, pasta final em `saida/` (capa.jpg + legenda.txt), RENDER.bat
   e checagem final (duração, capa 1080×1920, sem arquivos extras). Só copia MP4 de `saida/` se for MAIS NOVO que a última edição.
7. Render no Windows: usuário dá 2 cliques em `episodios\cafe-contado\<EP>\RENDER.bat` (renderiza ~8 min e copia o MP4 para a pasta final em `saida/`).
   Na VM o render leva ~95 min: não usar. Depois do render NÃO mexer no episódio (qualquer edição torna o MP4 "antigo").
- Não explorar pastas de outros episódios nem `ferramentas/` além do necessário. `ls` antes de abrir qualquer arquivo incerto.
- Na VM não dá para apagar nem mover entre pastas (vira cópia): renomear no lugar ou deixar para o usuário.

## cenas.js — cabeçalho
```
// DUR: <fim da narração + 1.4>
// CTA: <tempo da frase-gatilho do CTA; legendas somem aqui> (vira `const CTA` automaticamente: NÃO declarar no cenas.js)
// KEY: palavra1, palavra2 (fita vermelha na legenda; minúsculas, com acento)
// PECAS: apelido=arquivo apelido2=arquivo2 (arquivo = nome do PNG sem .png, lista abaixo)
// SELO: EP.2   (OBRIGATÓRIO; texto do selo vermelho do canto, escolhido pelo usuário: EP.1, EP.2…, CURIOSIDADE… ou NENHUM = sem selo)
```
Já carregados sem declarar: newsA, newsB, hand, nface/njaw (boneco who:'n'). Papéis: 'kraft' 'cream' 'red' 'green' 'split'.

## Atalhos (usar SEMPRE — padrões da casa já embutidos; `o` sobrescreve qualquer campo)
```
RAN(texto, x, y, size, in, o)        ransom (r -3, letra a letra, pal/fonts da casa)
TAG(texto, x, y, size, in, bg=GOLD, o)   etiqueta (r -2, fg automático: CREAM em INK/RED)
FAI(texto, x, y, size, in, bg=INK, o)    faixa Anton (largura/altura automáticas, slideL)
FIG(apelido, x, y, s, in, o)         imagem (slap)            SEL(texto, x, y, R, in, o)  selo (r 10, CREAM)
in = 0 → entra sem animação.  Cores: INK RED CREAM GOLD.  Papéis: 'kraft' 'cream' 'red' 'green' 'split'.
```
Esqueleto (não é preciso ler episódios antigos):
```
// DUR: 100.9
// CTA: 95.0
// KEY: café, cafeína
// PECAS: cup=cup sugar=sugar
// SELO: CURIOSIDADE
scene('kraft', 0, 5.0, [
  RAN('CAFÉ\nEMAGRECE?', 540, 520, 104, 0),
  FIG('cup', 790, 980, 0.75, 0, { r: 6 }),
  TAG('ENGORDA FÁCIL?', 540, 1520, 70, 1.4),
  FAI('TOMA MAIS CAFÉ', 540, 1720, 76, 3.5, RED, { r: 2 }),
], { cam: [[0, 1.0, 540, 960], [3.2, 1.05, 540, 1100, 1.6]] });
// ... cenas ... ; CTA: scene('kraft', CTA, DUR + 1, [ E({ k:'mimg', img:'cup', x:540, y:2200, s:0.9, in:CTA, anim:'none', mv:[CTA, CTA+0.9, 0, -700, -6] }), RAN(...), FAI(...), E({ k:'btn', text:'COMPARTILHA', x:540, y:1260, in:..., size:72 }) ], {...})
function CAPA_SCENE() { scene('kraft', 0, DUR + 1, [ RAN(...,0), FIG(...,0), FAI(...,0) ], { cam: [[0, 1.0, 540, 960]] }); }
```
Outros elementos (via `E({ k, x, y, s, r, in, anim, ... })`; anim 'slap' 'drop' 'slideL' 'slideR' 'grow' 'none'; `still: true` em fundo; `filter: GRAY`):
mimg + `mv:[t0,t1,dx,dy,drot]` · arrow `{x0,y0,x1,y1,bend:[dx,dy]}` · circle `{rx,ry}` · btn `{text,size}` · heart · bubble `{text,tail}`
route `{x:540,y:900,pts:[[x,y,t],[x2,y2,t2,dur]],bend:[n]}` · cherry `{col,label}` · lurdes `{who:'n',talk:[]}`
Já carregados sem PECAS: newsA, newsB, hand. `const GRAY = 'grayscale(1) contrast(1.1) brightness(0.9)'` deve ser declarado no cenas.js se usado.
Câmera: `{ cam: [[t, zoom, cx, cy], [t, zoom, cx, cy, dur]] }` — zoom ≤ 1.08 com texto nas bordas.

## Regras de layout (erros que já aconteceram)
- Selo (quando houver) ocupa o canto sup. esquerdo (até x 330, y 220): nada de texto ali; manchetes em y ≥ 380.
- Legenda fixa em y 1150–1350: etiquetas fora dessa faixa.
- ransom: ~9 letras por linha → size ≤ 104; "100 PONTOS" (10) → size 92. Zoom > 1.1 corta ransom/strip largos.
- Etiquetas vizinhas: ≥ 180 px de distância vertical.
- Título de tela visível de 0 a 3 s; câmera parada (zoom 1.0) até 3 s.
- CTA Café Contado: ransom "SEGUE A\nPÁGINA" / "MANDA PRA\nESSA PESSOA" + btn "+ SEGUE" ou "COMPARTILHA". Sem "FIM DO EPISÓDIO".
- Capa (CAPA_SCENE): tudo entre y 300 e 1620 (grade do perfil), sem legenda.

## Mapas (img em s 1.0, centro (540, 900) → worldmap; s 1.15 → brmap)
worldmap: Brasil (325,870) · Congo (701,871) · Bruxelas/Europa (641,506)
brmap: RO (245,805) · PR (482,1203) · MG (712,1038) · BA (793,900) · GO (609,1061) · SP (655,1250) · ES (880,1120)
Partes do mundo no mesmo estilo (s 1.0, centro (540, 900)): mapa_europa = Europa + norte da África + Oriente Médio · mapa_asia = Ásia + Oceania · mapa_mundo = mundo inteiro (faixa baixa, só p/ visão geral). Com s ≠ 1: x = 540 + (x₁ − 540)·s, y = 900 + (y₁ − 900)·s.
mapa_europa: Portugal (206,906) · Espanha (257,896) · França (328,803) · Reino Unido (277,706) · Bélgica (352,742) · Holanda (364,717) · Alemanha (419,736) · Suíça (394,799) · Itália (443,859) · Polônia (522,721) · Suécia (483,564) · Noruega (403,579) · Finlândia (597,557) · Grécia (551,908) · Ucrânia (654,766) · Turquia (700,915) · Rússia (815,647) · Marrocos (231,1020) · Argélia (334,1080) · Egito (643,1102) · Arábia Saudita (815,1139) · Dubai (932,1122) · Irã (906,1020)
mapa_asia: Índia (217,762) · China (419,657) · Mongólia (411,560) · Coreia do Sul (611,646) · Japão (697,645) · Vietnã (438,815) · Tailândia (395,819) · Filipinas (564,843) · Indonésia (524,957) · Austrália (661,1143) · Nova Zelândia (967,1273)
mapa_mundo: Brasil (373,958) · EUA (245,824) · México (234,867) · Colômbia (313,919) · Portugal (490,822) · Espanha (503,820) · França (520,803) · Reino Unido (507,785) · Bélgica (525,792) · Holanda (528,787) · Alemanha (541,791) · Suíça (535,802) · Itália (547,813) · Polônia (566,788) · Suécia (556,759) · Noruega (537,762) · Finlândia (584,758) · Grécia (573,822) · Ucrânia (597,796) · Turquia (608,824) · Rússia (636,774) · Marrocos (496,843) · Argélia (521,854) · Egito (595,858) · Etiópia (621,907) · Arábia Saudita (636,865) · Dubai (664,861) · Irã (658,843) · Índia (729,870) · China (797,835) · Mongólia (794,802) · Coreia do Sul (862,831) · Japão (891,830) · Vietnã (803,888) · Tailândia (789,889) · Filipinas (846,897) · Indonésia (832,936) · Austrália (879,999) · Nova Zelândia (983,1042) · África do Sul (578,1009) · Quênia (616,930) · Canadá (223,772)

## Peças novas
Só se faltar e tiver função narrativa. NÃO ler outros geradores: usar `ferramentas/geradores-de-imagens/pecas.py`
(`canvas, S, finish(im, nome, categoria), registrar([nomes], categoria, EP)` — exemplo pronto em `geradores-de-imagens/cafe-emagrece/prep_emagrece.py`).
Criar `geradores-de-imagens/<ep>/prep_<ep>.py`, rodar, e ver as peças no próprio contato da prévia (sem folha separada).

## Escala (s) que funciona — evita rodada de ajuste
- objetos médios (cup, espresso, teacup, flask, microscope, sugar, bathscale): 0.6–0.9 · em grupo de 3: 0.5–0.6
- ícones pequenos de origem (flame0/1, gear, milk, bolt, thermo): flame/gear 1.5–2.2 · milk/bolt/thermo 0.6
- breadL/breadR lado a lado: 0.9 (x 380 / 700) · fundos/mapas: 0.92–1.15

## Peças disponíveis (arquivo para PECAS)
- **amazonia**: bg_amazonia castanha chocolate frutas
- **cenarios**: bg_auction bg_blackfrost bg_busin bg_cerrado bg_cupping bg_dubai bg_exchange bg_field bg_frost bg_parana bg_road bg_roast bg_sitio bg_town
- **espaco**: astro astro2 bg_space capsule clock coffeemaker drop0 drop1 drop2 flask gear iss pouch socket spacemachine table
- **extras-estilo-original**: bfly_a bfly_b bird_hawk earth flame0 flame1 rocket rose_centi rose_purple
- **lavoura-e-clima**: br_arabica br_conilon campo cloud coldfront field flake flower forest leaf0 leaf1 leaf2 leaf3 leaf4 leaf5 leaf6 leaf7 leafspot lowland mountains rust seeds snow sprout sun tree waves worm
- **mapas**: brmap map2 worldmap mapa_europa mapa_asia mapa_mundo
- **objetos**: bathscale bolt sugar balance bank basket bee board br_eugen breadL breadR bus cage camera car chatphone chromo_a chromo_b civet coins comment cow crown cup dice dna espresso fazenda gate gavel handshake harvester jar laptop lotlabel lupa medal microscope milk money paddle0 paddle1 paddle2 paddle3 paddle4 paddle5 padlock phone pickup pie34 pie63 piggy plane podium qblob roast sack_a sack_b score ship shop sign specbag stairs suitcase teacup thermo ticket tray trophy warehouse wheel worker0 worker1 worker2 worker3
- **recortes-de-jornal**: manicule news_a news_b space_wedge
- **bonecos (lurdes who:)**: n (neto, já carregado). Outros exigem carregar face/jaw — evitar.
