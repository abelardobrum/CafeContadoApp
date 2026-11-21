import { useEffect, useMemo, useRef, useState } from 'react';
import Config from './Config.jsx';

const SELOS = ['EP.1', 'EP.2', 'EP.3', 'EP.4', 'EP.5', 'CURIOSIDADE', 'NENHUM'];
const FASES = [
  ['claude', 'Claude montando as cenas'],
  ['render', 'Renderizando o vídeo'],
  ['pronto', 'Entregue em saida/'],
];

export default function App() {
  const [saude, setSaude] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [aba, setAba] = useState('produzir');

  const atualizar = () =>
    fetch('/api/saude').then((r) => r.json()).then((s) => {
      setSaude(s);
      if (s.atual) setJobId(s.atual.id);
      return s;
    }).catch(() => setSaude({ offline: true }));

  useEffect(() => {
    atualizar().then((s) => { if (s && s.claude && !s.claude.pronto) setAba('config'); });
  }, []);

  const claudeOk = saude?.claude?.pronto;

  return (
    <div className="pagina">
      <header className="topo">
        <div>
          <h1>CAFÉ CONTADO</h1>
          <p className="sub">estúdio de episódios · Claude + kit de colagem</p>
        </div>
        <Saude s={saude} onClaude={() => setAba('config')} />
      </header>
      <nav className="abas" role="tablist">
        <button role="tab" aria-selected={aba === 'produzir'} className={aba === 'produzir' ? 'ativa' : ''} onClick={() => setAba('produzir')}>Produzir</button>
        <button role="tab" aria-selected={aba === 'config'} className={aba === 'config' ? 'ativa' : ''} onClick={() => setAba('config')}>
          Configuração{saude && !saude.offline && !claudeOk && <i className="ponto" aria-label="pendente" />}
        </button>
      </nav>
      <main className="grade" hidden={aba !== 'produzir'}>
        <Formulario
          ocupado={Boolean(jobId && saude?.atual?.id === jobId)}
          semClaude={saude && !saude.offline && !claudeOk}
          onIrConfig={() => setAba('config')}
          onCriado={(j) => { setJobId(j.id); setSaude((s) => ({ ...s, atual: j })); }}
        />
        <Painel jobId={jobId} onFim={() => setSaude((s) => ({ ...s, atual: null }))} />
      </main>
      {aba === 'config' && <Config onMudou={atualizar} />}
    </div>
  );
}

function Saude({ s, onClaude }) {
  if (!s) return <div className="saude">verificando…</div>;
  if (s.offline) return <div className="saude ruim">servidor desligado — abra o ABRIR-ESTUDIO.bat</div>;
  const itens = [['kit', s.kit], ['ffmpeg', s.ffmpeg], ['python', s.python], ['chrome', s.chrome]];
  const c = s.claude || {};
  return (
    <div className="saude">
      {itens.map(([n, ok]) => <span key={n} className={ok ? 'ok' : 'ruim'}>{ok ? '●' : '○'} {n}</span>)}
      <button className={'chip ' + (c.pronto ? 'ok' : 'ruim')} onClick={onClaude} title="Abrir configuração do Claude">
        {c.pronto ? '●' : '○'} claude{c.pronto ? ` · ${c.modelo?.replace('claude-', '')}` : ' · entrar'}
      </button>
    </div>
  );
}

function Formulario({ ocupado, semClaude, onIrConfig, onCriado }) {
  const [titulo, setTitulo] = useState('');
  const [selo, setSelo] = useState('');
  const [copy, setCopy] = useState('');
  const [prompt, setPrompt] = useState('');
  const [narracao, setNarracao] = useState(null);
  const [musica, setMusica] = useState(null);
  const [renderizar, setRenderizar] = useState(true);
  const [erro, setErro] = useState('');
  const [enviando, setEnviando] = useState(false);

  async function enviar(e) {
    e.preventDefault();
    setErro('');
    const fd = new FormData();
    fd.append('titulo', titulo);
    fd.append('selo', selo);
    fd.append('copy', copy);
    fd.append('prompt', prompt);
    fd.append('renderizar', renderizar ? '1' : '0');
    if (narracao) fd.append('narracao', narracao);
    if (musica) fd.append('musica', musica);
    setEnviando(true);
    try {
      const r = await fetch('/api/jobs', { method: 'POST', body: fd });
      const j = await r.json();
      if (!r.ok) throw new Error(j.erro || 'Falha ao enviar');
      onCriado(j);
    } catch (e2) {
      setErro(e2.message);
    } finally {
      setEnviando(false);
    }
  }

  const pronto = titulo.trim() && selo.trim() && copy.trim() && narracao && musica;

  return (
    <form className="cartao form" onSubmit={enviar}>
      <h2>Novo episódio</h2>

      <label className="campo">
        <span>Título do vídeo</span>
        <input value={titulo} onChange={(e) => setTitulo(e.target.value)} placeholder="Ex.: Café emagrece?" maxLength={90} />
      </label>

      <label className="campo">
        <span>Selo <em>canto superior esquerdo</em></span>
        <input list="selos" value={selo} onChange={(e) => setSelo(e.target.value)} placeholder="EP.5, CURIOSIDADE ou NENHUM" />
        <datalist id="selos">{SELOS.map((s) => <option key={s} value={s} />)}</datalist>
      </label>

      <label className="campo">
        <span>Copy <em>roteiro da narração</em></span>
        <textarea rows={8} value={copy} onChange={(e) => setCopy(e.target.value)} placeholder="Cole aqui o texto narrado…" />
      </label>

      <div className="duplo">
        <Arquivo rotulo="Áudio da narração" arq={narracao} onArq={setNarracao} />
        <Arquivo rotulo="Música de fundo" arq={musica} onArq={setMusica} />
      </div>

      <label className="campo">
        <span>Prompt adicional <em>opcional</em></span>
        <textarea rows={4} value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Ex.: usar o mapa do Brasil na cena de Minas, tom mais bem-humorado, CTA de compartilhar…" />
      </label>

      <label className="check">
        <input type="checkbox" checked={renderizar} onChange={(e) => setRenderizar(e.target.checked)} />
        Renderizar o MP4 no final (~8 min)
      </label>

      {erro && <p className="aviso">{erro}</p>}
      {semClaude && <p className="aviso">O Claude ainda não está conectado. <button type="button" className="link" onClick={onIrConfig}>Ir para Configuração</button></p>}
      <button className="botao" disabled={!pronto || enviando || ocupado || semClaude}>
        {ocupado ? 'Produzindo…' : enviando ? 'Enviando…' : 'Produzir episódio'}
      </button>
    </form>
  );
}

function Arquivo({ rotulo, arq, onArq }) {
  const ref = useRef(null);
  const [sobre, setSobre] = useState(false);
  const url = useMemo(() => (arq ? URL.createObjectURL(arq) : null), [arq]);
  useEffect(() => () => url && URL.revokeObjectURL(url), [url]);
  return (
    <div
      className={'arquivo' + (sobre ? ' sobre' : '') + (arq ? ' cheio' : '')}
      onClick={() => !arq && ref.current.click()}
      onDragOver={(e) => { e.preventDefault(); setSobre(true); }}
      onDragLeave={() => setSobre(false)}
      onDrop={(e) => { e.preventDefault(); setSobre(false); const f = e.dataTransfer.files[0]; if (f) onArq(f); }}
    >
      <span className="rot">{rotulo}</span>
      <input ref={ref} type="file" accept="audio/*" hidden onChange={(e) => onArq(e.target.files[0] || null)} />
      {arq ? (
        <>
          <span className="nome" title={arq.name}>{arq.name}</span>
          <audio controls src={url} />
          <button type="button" className="link" onClick={(e) => { e.stopPropagation(); onArq(null); }}>trocar</button>
        </>
      ) : (
        <span className="dica">arraste o arquivo ou clique<br />(mp3, wav, m4a…)</span>
      )}
    </div>
  );
}

function Painel({ jobId, onFim }) {
  const [job, setJob] = useState(null);
  const [eventos, setEventos] = useState([]);
  const [previa, setPrevia] = useState(0);
  const fim = useRef(null);

  useEffect(() => {
    if (!jobId) return;
    setEventos([]);
    const es = new EventSource(`/api/jobs/${jobId}/eventos`);
    es.onmessage = (m) => {
      const ev = JSON.parse(m.data);
      if (ev.tipo === 'estado') {
        setJob(ev);
        if (ev.status !== 'rodando') onFim();
      } else if (ev.tipo === 'previa') {
        setPrevia(Date.now());
      } else if (ev.tipo === 'progresso') {
        setJob((j) => (j ? { ...j, progresso: ev.valor } : j));
        setEventos((l) => (l.at(-1)?.tipo === 'progresso' ? [...l.slice(0, -1), ev] : [...l, ev]));
      } else {
        setEventos((l) => [...l, ev]);
      }
    };
    return () => es.close();
  }, [jobId]);

  useEffect(() => { fim.current?.scrollIntoView({ block: 'nearest' }); }, [eventos.length]);

  if (!jobId) {
    return (
      <section className="cartao painel vazio">
        <h2>Como funciona</h2>
        <ol>
          <li>Os arquivos vão para <code>entrada/&lt;slug&gt;/</code> do kit.</li>
          <li>O Claude segue o <code>CAFE-CONTADO.md</code>: cria o episódio, escreve as cenas, confere a prévia e finaliza.</li>
          <li>O app renderiza e entrega em <code>saida/&lt;Selo&gt; - &lt;Título&gt;/</code> (MP4, capa e legenda).</li>
        </ol>
      </section>
    );
  }

  const fase = job?.fase || 'claude';
  const idx = FASES.findIndex(([f]) => f === fase);
  const rodando = job?.status === 'rodando';

  return (
    <section className="cartao painel">
      <div className="cab">
        <div>
          <h2>{job?.titulo || '…'}</h2>
          <p className="meta">{job?.selo} · EP {job?.ep}{job?.custo != null && ` · US$ ${job.custo.toFixed(2)}`}</p>
        </div>
        {rodando && <button className="botao fino" onClick={() => fetch(`/api/jobs/${jobId}/cancelar`, { method: 'POST' })}>Cancelar</button>}
      </div>

      <ol className="fases">
        {FASES.filter(([f]) => f !== 'render' || job?.renderizar !== false).map(([f, nome]) => {
          const i = FASES.findIndex(([x]) => x === f);
          const st = job?.status === 'ok' || i < idx ? 'feito' : i === idx ? (rodando ? 'agora' : job?.status) : '';
          return (
            <li key={f} className={st}>
              {nome}
              {f === 'render' && fase === 'render' && job?.progresso != null && <span className="barra"><i style={{ width: `${job.progresso * 100}%` }} /></span>}
            </li>
          );
        })}
      </ol>

      {job?.erro && <p className="aviso">{job.erro}</p>}
      {job?.status === 'ok' && (
        <div className="entrega">
          <span>Pasta final: <code>{job.pasta}</code></span>
          <button className="botao fino" onClick={() => fetch(`/api/jobs/${jobId}/abrir-pasta`, { method: 'POST' })}>Abrir pasta</button>
        </div>
      )}

      {(previa > 0 || job?.status === 'ok') && (
        <figure className="previa">
          <img src={`/api/jobs/${jobId}/imagem/contato?v=${previa}`} alt="Folha de contato: um quadro por cena e a capa" onError={(e) => (e.currentTarget.style.display = 'none')} />
          <figcaption>prévia · um quadro por cena + capa</figcaption>
        </figure>
      )}

      <div className="log">
        {eventos.map((ev, i) => <Linha key={i} ev={ev} />)}
        <div ref={fim} />
      </div>
    </section>
  );
}

function Linha({ ev }) {
  if (ev.tipo === 'claude') return <div className="l claude">{ev.texto}</div>;
  if (ev.tipo === 'ferramenta') return <div className="l ferr"><b>{ev.nome}</b> {ev.texto}</div>;
  if (ev.tipo === 'saida') return <details className="l saida"><summary>{ev.texto.split('\n')[0].slice(0, 110)}</summary><pre>{ev.texto}</pre></details>;
  if (ev.tipo === 'erro') return <div className="l erro">{ev.texto}</div>;
  if (ev.tipo === 'progresso') return <div className="l info">{ev.texto}</div>;
  return <div className={`l ${ev.tipo}`}>{ev.texto}</div>;
}
