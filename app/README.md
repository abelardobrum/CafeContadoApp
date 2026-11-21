# Café Contado · Estúdio (app)

Tela web para produzir episódios com o `kit-cafe-contado` usando o Claude.

```
(na pasta principal) INSTALAR.bat   # uma vez: kit + estudio + ffmpeg + Claude Code
npm run dev        # desenvolvimento: http://localhost:5173
npm start          # build + servidor único: http://localhost:3001
```

**Fluxo:** o formulário grava `copy.txt`, `narr.mp3` e `musica.mp3` em `kit-cafe-contado/entrada/<slug>/`
(outros formatos de áudio são convertidos para mp3). Em seguida, o servidor abre uma sessão do Claude
(Claude Agent SDK) dentro da pasta do kit. A sessão segue o `CAFE-CONTADO.md`: `cc.py novo`, escreve
`cenas.js` e `legenda.txt`, roda `previa`, confere o contato, roda `ajustar` se precisar e termina com `finalizar`.
Depois o app renderiza com `motor/render.mjs` e copia o MP4 para `saida/<Selo> - <Título>/`.
O log de cada episódio fica em `entrada/<slug>/log.txt`.

**Claude:** usa o login do Claude Code desta máquina. Sem login, coloque `ANTHROPIC_API_KEY` no `.env`
Login, chave, modelo, esforço e processos do render ficam na aba **Configuração** (salvos em `.env`).

**Requisitos:** Node 18+, Python 3, Chrome, e ffmpeg/ffprobe em `kit-cafe-contado/motor/tools/`.
