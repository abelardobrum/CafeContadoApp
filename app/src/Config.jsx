import { useEffect, useRef, useState } from 'react';

const NOMES_MODELO = {
  'claude-opus-5-5': 'Claude Opus 5.5 — padrão, melhor custo-benefício',
  'claude-sonnet-5-5': 'Claude Sonnet 5.5 — mais rápido e barato',
  'claude-fable-5-2': 'Claude Fable 5.2 — o mais capaz, mais caro',
};
const NOMES_ESFORCO = { low: 'baixo', medium: 'médio', high: 'alto (recomendado)', xhigh: 'muito alto', max: 'máximo' };

async function api(url, opts = {}) {
  const r = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...opts });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.erro || `Erro ${r.status}`);
  return j;
}

export default function Config({ onMudou }) {
  const [st, setSt] = useState(null);
  const [cfg, setCfg] = useState(null);
  const [esperandoLogin, setEsperandoLogin] = useState(false);
  const [teste, setTeste] = useState(null);
  const [msg, setMsg] = useState('');
  const [erro, setErro] = useState('');
  const [chave, setChave] = useState('');
  const timer = useRef(null);

  const carregarStatus = () => api('/api/claude/status').then((s) => { setSt(s); return s; });

  useEffect(() => {
    carregarStatus().catch((e) => setErro(e.message));
    api('/api/config').then(setCfg).catch((e) => setErro(e.message));
    return () => clearInterval(timer.current);
  }, []);

  async function entrar(modo) {
    setErro(''); setMsg('');
    try {
      await api('/api/claude/login', { method: 'POST', body: JSON.stringify({ modo }) });
      setEsperandoLogin(true);
      clearInterval(timer.current);
      let n = 0;
      timer.current = setInterval(async () => {
        const s = await carregarStatus().catch(() => null);
        if (s?.conta || ++n > 150) {
          clearInterval(timer.current);
          setEsperandoLogin(false);
          if (s?.conta) { setMsg('Login feito.'); onMudou(); }
        }
      }, 2000);
    } catch (e) { setErro(e.message); }
  }

  async function sair() {
    if (!confirm('Sair da conta do Claude neste computador? Isso também desconecta o Claude Code no terminal.')) return;
    setErro(''); setMsg('');
    try { setSt(await api('/api/claude/sair', { method: 'POST' })); onMudou(); } catch (e) { setErro(e.message); }
  }

  async function testar() {
    setErro(''); setTeste({ rodando: true });
    try { setTeste(await api('/api/claude/testar', { method: 'POST' })); } catch (e) { setTeste(null); setErro(e.message); }
  }

  async function salvar(patch, aviso = 'Salvo.') {
    setErro(''); setMsg('');
    try {
      setCfg(await api('/api/config', { method: 'PUT', body: JSON.stringify(patch) }));
      setMsg(aviso);
      await carregarStatus();
      onMudou();
    } catch (e) { setErro(e.message); }
  }

  return (
    <main className="config">
      <section className="cartao">
        <h2>Conexão com o Claude</h2>
        {!st ? <p className="meta">verificando…</p> : (
          <>
            <div className={'estado ' + (st.pronto ? 'ok' : 'ruim')}>
              <b>{st.pronto ? 'Conectado' : 'Não conectado'}</b>
              <span>
                {st.metodo === 'chave' && <>usando a chave de API <code>{st.chave}</code>{st.conta && ' (ela tem prioridade sobre a conta)'}</>}
                {st.metodo === 'conta' && <>conta {st.conta.email}{st.conta.plano && ` · plano ${st.conta.plano}`}</>}
                {!st.metodo && 'Entre com sua conta do Claude ou cadastre uma chave de API abaixo.'}
              </span>
            </div>

            <h3>Conta do Claude (Pro / Max)</h3>
            <p className="meta">Usa o mesmo login do Claude Code. Os episódios gastam do limite do seu plano.</p>
            {!st.cli && <p className="aviso">O Claude Code não está instalado neste computador. Instale em claude.com/claude-code ou use uma chave de API.</p>}
            <div className="acoes">
              {st.conta ? (
                <button className="botao fino" onClick={sair}>Sair da conta</button>
              ) : (
                <>
                  <button className="botao fino" disabled={!st.cli || esperandoLogin} onClick={() => entrar('claudeai')}>Entrar com conta Claude</button>
                  <button className="botao fino claro" disabled={!st.cli || esperandoLogin} onClick={() => entrar('console')}>Entrar com Console (API)</button>
                </>
              )}
              {st.pronto && <button className="botao fino claro" disabled={teste?.rodando} onClick={testar}>{teste?.rodando ? 'Testando…' : 'Testar conexão'}</button>}
            </div>
            {esperandoLogin && (
              <p className="dica-login">Abri uma janela de login. Autorize no navegador; se a janela pedir um código, cole lá. Esta tela atualiza sozinha.</p>
            )}
            {teste && !teste.rodando && (
              <p className="sucesso">Claude respondeu "{teste.resposta}" em {teste.segundos.toFixed(1)} s · {teste.modelo}</p>
            )}

            <h3>Chave de API <em>opcional</em></h3>
            <p className="meta">Para cobrar no Console da Anthropic em vez do plano. Fica salva só em <code>app/.env</code>.</p>
            <form className="linha" onSubmit={(e) => { e.preventDefault(); salvar({ chave }, 'Chave salva.'); setChave(''); }}>
              <input type="password" value={chave} onChange={(e) => setChave(e.target.value)} placeholder={st.chave || 'sk-ant-…'} autoComplete="off" />
              <button className="botao fino" disabled={!chave.trim()}>Salvar</button>
              {st.chave && <button type="button" className="botao fino claro" onClick={() => salvar({ chave: '' }, 'Chave removida.')}>Remover</button>}
            </form>
          </>
        )}
      </section>

      <section className="cartao">
        <h2>Produção</h2>
        {!cfg ? <p className="meta">carregando…</p> : (
          <>
            <label className="campo">
              <span>Modelo</span>
              <select value={cfg.modelo} onChange={(e) => salvar({ modelo: e.target.value })}>
                {cfg.modelos.map((m) => <option key={m} value={m}>{NOMES_MODELO[m] || m}</option>)}
              </select>
            </label>
            <label className="campo">
              <span>Esforço <em>quanto o Claude pensa em cada passo</em></span>
              <select value={cfg.esforco} onChange={(e) => salvar({ esforco: e.target.value })}>
                {cfg.esforcos.map((x) => <option key={x} value={x}>{NOMES_ESFORCO[x] || x}</option>)}
              </select>
            </label>
            <label className="campo">
              <span>Processos do render <em>mais = mais rápido, mais pesado</em></span>
              <input type="number" min={1} max={32} defaultValue={cfg.workers} onBlur={(e) => Number(e.target.value) !== cfg.workers && salvar({ workers: e.target.value })} />
            </label>
            <p className="meta">As mudanças valem para o próximo episódio.</p>
          </>
        )}
      </section>

      {(msg || erro) && <p className={erro ? 'aviso' : 'sucesso'} style={{ gridColumn: '1 / -1' }}>{erro || msg}</p>}
    </main>
  );
}
