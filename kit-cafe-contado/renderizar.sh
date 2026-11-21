#!/usr/bin/env bash
# Renderiza um episódio (macOS/Linux).  Uso: ./renderizar.sh EX-01 [processos]
set -e
cd "$(dirname "$0")"
EP_NAME="$1"; W="${2:-4}"
[ -z "$EP_NAME" ] && { echo "Uso: ./renderizar.sh EX-01 [processos]"; exit 1; }
EP=$(ls -d episodios/*/"$EP_NAME" 2>/dev/null | head -1)
[ -z "$EP" ] && { echo "Episódio $EP_NAME não encontrado em episodios/"; exit 1; }
if [ -z "$MG_CHROME" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser; do
    [ -x "$c" ] && export MG_CHROME="$c" && break
  done
fi
mkdir -p saida
node motor/render.mjs "$EP" --audio "$EP/audio.flac" --out "saida/$EP_NAME.mp4" --workers "$W"
echo "Pronto: saida/$EP_NAME.mp4"
