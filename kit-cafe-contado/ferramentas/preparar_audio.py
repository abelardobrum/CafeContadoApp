import argparse, json, os, re, subprocess, sys, tempfile
import numpy as np

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(*a, **k):
    return subprocess.run(list(a), check=True, capture_output=True, text=True, **k)

def duracao(p):
    return float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p).stdout)

def legendas(ep):
    narr = os.path.join(ep, 'narr.mp3')
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', narr, '-af', 'silencedetect=n=-35dB:d=0.2', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    sil = re.findall(r'(silence_start|silence_end): ([0-9.]+)', log)
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, 'sil.txt'), 'w').write('\n'.join(f'{k}: {v}' for k, v in sil) + '\n')
        open(os.path.join(td, 'dur.txt'), 'w').write(str(duracao(narr)))
        open(os.path.join(td, 'text.txt'), 'w', encoding='utf-8').write(open(os.path.join(ep, 'roteiro.txt'), encoding='utf-8').read())
        run(sys.executable, os.path.join(KIT, 'ferramentas', 'alinhar_legendas.py'), cwd=td)
        os.replace(os.path.join(td, 'words.json'), os.path.join(ep, 'words.json'))
    w = json.load(open(os.path.join(ep, 'words.json')))
    print(f'words.json: {len(w)} palavras, narração de {duracao(narr):.2f} s')

def envelope(ep):
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(ep, 'narr.mp3'), '-ac', '1', '-ar', '48000',
                                      '-f', 'f32le', '-'], capture_output=True, check=True).stdout, dtype=np.float32)
    H = 4000; n = len(x) // H
    r = np.sqrt((x[:n * H].reshape(n, H) ** 2).mean(1))
    json.dump([round(float(a), 3) for a in np.clip(r / np.percentile(r, 95), 0, 1)], open(os.path.join(ep, 'env.json'), 'w'))
    print('env.json ok')

def mix(ep, musica):
    html = open(os.path.join(ep, 'index.html'), encoding='utf-8').read()
    D = float(re.search(r'DUR = ([\d.]+)', html).group(1))
    run(sys.executable, os.path.join(KIT, 'ferramentas', 'gerar_efeitos.py'), ep)
    with tempfile.TemporaryDirectory() as td:
        v, pm = os.path.join(td, 'voice.wav'), os.path.join(td, 'premix.wav')
        run('ffmpeg', '-v', 'error', '-y', '-i', os.path.join(ep, 'narr.mp3'), '-af',
            'highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2:LRA=9', '-ar', '48000', '-ac', '2', v)
        sfx = os.path.join(ep, 'sfx.wav')
        if not musica: 
            ins = ['-i', v, '-i', sfx]
            fc = f'[1:a]volume=-14dB[s];[0:a][s]amix=inputs=2:duration=longest:normalize=0,atrim=0:{D}[o]'
        else:
            ins = ['-i', v, '-i', musica, '-i', sfx]
            fc = (f'[1:a]atrim=0:{D},asetpts=N/SR/TB,aresample=48000,afade=t=in:d=1.2,afade=t=out:st={D - 2.4:.2f}:d=2.4,volume=-11dB[m];'
                  '[0:a]asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=300[md];'
                  f'[2:a]volume=-14dB[s];[v][md][s]amix=inputs=3:duration=longest:normalize=0,atrim=0:{D}[o]')
        run('ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '[o]', '-ar', '48000', pm)
        js = subprocess.run(['ffmpeg', '-hide_banner', '-i', pm, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                            capture_output=True, text=True).stderr
        m = json.loads(js[js.rindex('{'):js.rindex('}') + 1])
        af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
              f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
        run('ffmpeg', '-v', 'error', '-y', '-i', pm, '-af', af, '-ar', '48000', '-c:a', 'flac', os.path.join(ep, 'audio.flac'))
    os.remove(os.path.join(ep, 'sfx.wav'))
    print(f'audio.flac ok ({D} s, −14 LUFS)')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('episodio'); ap.add_argument('--musica'); ap.add_argument('--so-legendas', action='store_true')
    a = ap.parse_args()
    legendas(a.episodio); envelope(a.episodio)
    if not a.so_legendas:
        mix(a.episodio, a.musica)
