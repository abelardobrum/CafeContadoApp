"""Cria a pasta de um episódio novo a partir do modelo.

Uso:
  python ferramentas/novo_episodio.py <serie> <EP> --narracao caminho/narr.mp3 --roteiro caminho/copy.txt [--selo "EP. 1"]
Ex.:
  python ferramentas/novo_episodio.py serie-4-xxx ST4-PT1 --narracao ~/Downloads/pt1.mp3 --roteiro copy.txt --selo "EP. 1"

Depois: preparar_audio.py --so-legendas → escrever as cenas no index.html (tempos do words.json)
        → preparar_audio.py --musica ... → renderizar.bat <EP>
"""
import argparse, os, shutil, subprocess, json, re
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('serie'); ap.add_argument('ep'); ap.add_argument('--narracao', required=True); ap.add_argument('--roteiro', required=True)
ap.add_argument('--selo', default=None)
a = ap.parse_args()
rel = f'episodios/{a.serie}/{a.ep}'; pasta = os.path.join(KIT, rel)
if os.path.exists(os.path.join(pasta, 'index.html')): raise SystemExit(f'{rel} já existe')
os.makedirs(pasta, exist_ok=True)
shutil.copy(a.narracao, os.path.join(pasta, 'narr.mp3'))
shutil.copy(a.roteiro, os.path.join(pasta, 'roteiro.txt'))
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.narracao],
                           capture_output=True, text=True, check=True).stdout)
s = open(os.path.join(KIT, 'modelos', 'episodio-modelo', 'index.html'), encoding='utf-8').read()
selo = a.selo or ('EP. ' + re.sub(r'.*PT', '', a.ep))
s = (s.replace('__DUR__', f'{dur + 1.4:.1f}').replace('__FIM_LEGENDA__', f'{dur + 1.4:.2f}').replace('__PASTA__', rel)
      .replace('__SELO__', selo).replace('__PALAVRAS_CHAVE__', '').replace('__EP__', a.ep))
open(os.path.join(pasta, 'index.html'), 'w', encoding='utf-8').write(s)
print(f'criado {rel}  (DUR {dur + 1.4:.1f} s)')
