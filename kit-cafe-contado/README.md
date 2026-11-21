# Kit de colagem animada — reels verticais feitos por código

Kit para fazer reels verticais (1080×1920, 30 fps) em **colagem animada**: recortes de papel, letras de bilhete de resgate, bonecos que falam, mapas e gráficos de giz, câmera com zoom e efeitos de papel. Tudo é desenhado por código e renderizado quadro a quadro, sem IA de imagem ou vídeo. Nasceu nos reels do **Coffee Hub** (mercado de café) e já vem com uma biblioteca de 178 peças sobre café e agro.

**Antes de tudo, abra `catalogo.html`** no navegador para ver todas as peças.

## O que vem no kit

| Pasta | Conteúdo |
|---|---|
| `biblioteca/` | 15 cenários, 19 personagens, 73 objetos, lavoura e clima, mapas, recortes de jornal, papéis, texturas, fontes e efeitos sonoros |
| `episodios/exemplos/EX-01` | um episódio de exemplo pronto para renderizar |
| `modelos/episodio-modelo` | ponto de partida de um episódio novo |
| `motor/render.mjs` | renderizador (Chrome headless + ffmpeg) |
| `ferramentas/` | criar episódio, alinhar legendas, efeitos sonoros, mixagem −14 LUFS, atualizar catálogo |
| `skills/colagem-animada/` | skill para o Claude (Claude Code / claude.ai) fazer os vídeos com o kit |
| `GUIA-DO-KIT.md` | referência completa: cenas, câmera, todos os elementos, regras de estilo, checklist |

## Instalação

Precisa de: **Node.js 18+**, **Chrome** (ou Edge/Chromium), **ffmpeg** e, para as ferramentas de áudio, **Python 3** com `numpy` e `soundfile`.

```bash
git clone <este repositório> && cd <pasta>
npm install
pip install numpy soundfile
```

No Windows, `instalar.bat` faz o `npm install` e confere o ffmpeg (se não estiver no PATH, coloque `ffmpeg.exe` e `ffprobe.exe` em `motor\tools\`).

Teste com o exemplo:

```bash
./renderizar.sh EX-01          # macOS/Linux
renderizar.bat EX-01           # Windows
```

O vídeo sai em `saida/EX-01.mp4`.

## Fazer um episódio

```bash
python ferramentas/novo_episodio.py minha-serie EP01 --narracao narracao.mp3 --roteiro copy.txt --selo "EP. 1"
python ferramentas/preparar_audio.py episodios/minha-serie/EP01 --so-legendas
#  → escreva as cenas em episodios/minha-serie/EP01/index.html usando os tempos de words.json (veja GUIA-DO-KIT.md)
node motor/render.mjs episodios/minha-serie/EP01 --stills 2,10,30 --scale 0.3     # confere quadros em out/stills/
python ferramentas/preparar_audio.py episodios/minha-serie/EP01 --musica minha-musica.mp3   # --musica é opcional
./renderizar.sh EP01
```

Uma cena é assim:

```js
scene('kraft', 10.0, 16.1, [
  E({ k: 'img', img: 'bg_cerrado', x: 540, y: 960, s: 1.0, r: 0, in: 10.0, anim: 'none' }),     // cenário
  E({ k: 'lurdes', who: 'tonhovelho', x: 540, y: 1000, s: 0.8, r: -2, in: 10.3, talk: [] }),    // boneco que fala
  E({ k: 'tag', text: '500 MIL SACAS', x: 540, y: 420, size: 84, bg: GOLD, r: -3, in: 12.6 }),   // etiqueta
  E({ k: 'img', img: 'sackA', x: 300, y: 1450, s: 0.6, r: -5, in: 13.1, anim: 'drop' }),         // peça que cai
], { cam: [[10.0, 1.0, 540, 900], [12.4, 1.12, 540, 1050, 2.0]] });                              // zoom
```

## Com o Claude

Copie `skills/colagem-animada/` para a pasta de skills do Claude Code (`~/.claude/skills/`), ou envie a pasta como skill no claude.ai. Depois, peça algo como: *"faz um reel com esta narração e esta copy usando o kit de colagem"*.

## Licenças e créditos

- Código, ferramentas e peças desenhadas em código: **MIT** (ver `LICENSE`).
- Motor e estilo baseados em [mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15), de Vincentwei1021, sob licença MIT (`LICENSE.mg-styles-15`).
- Fotos, recortes de jornal, texturas e efeitos sonoros são de domínio público ou CC0. As fontes estão sob a SIL Open Font License (`biblioteca/fontes/LICENSE-*.txt`). Detalhes em `CREDITS.md`.
- A logo em `biblioteca/marca/` é marca do Coffee Hub e não está coberta pela licença MIT: troque pela sua.
- Os personagens são ilustrações genéricas desenhadas em código.
