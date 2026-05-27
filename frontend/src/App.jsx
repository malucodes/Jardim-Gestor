import { useState, useEffect } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import IconeMascotePadrao from './assets/mascote_padrao.svg';
import IconeMascotePlantar from './assets/mascote_nova_tarefa.svg';
import IconeMascoteRegar from './assets/mascote_atualizar.svg';
import IconeMascoteColher from './assets/mascote_concluidas.svg';
import IconeMascotePodar from './assets/mascote_deletar.svg';
import IconeCerca from './assets/cercas.svg'
import IconeEstufa from './assets/estufa.svg'
import IconeCalendario from './assets/calendario.svg'

import CardPlanta from './CardPlanta';
import FormularioPlantar from './FormularioPlantar';
import FormularioCuidar from './FormularioCuidar';
import FormularioPodar from './FormularioPodar';
import ConfirmacaoExclusaoModal from './ConfirmacaoExclusaoModal';
import './App.css';

function App() {
  const [sementes, setSementes] = useState([]);
  const [exibindoCesto, setExibindoCesto] = useState(false);
  const [modalPlantarAberto, setModalPlantarAberto] = useState(false);
  const [modalRegaAberto, setModalRegaAberto] = useState(false);
  const [modalPodarAberto, setModalPodarAberto] = useState(false);
  const [modalExclusaoCestoAberto, setModalExclusaoCestoAberto] = useState(false);
  const [sementeSelecionada, setSementeSelecionada] = useState("");
  const [mascoteAtual, setMascoteAtual] = useState(IconeMascotePadrao);

  const [googleToken, setGoogleToken] = useState(null);

  const conectarGoogle = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/tasks',
    onSuccess: (tokenResponse) => {
      setGoogleToken(tokenResponse.access_token);
      alert("Tarefas conectadas com sucesso! 🌿");
    },
    onError: (error) => console.log('Erro ao conectar:', error),
  });

  const reagirMascote = (imagemAcao) => {
    setMascoteAtual(imagemAcao);
    setTimeout(() => { setMascoteAtual(IconeMascotePadrao); }, 100000);
  };

  const carregarJardim = async () => {
    const resposta = await fetch('https://api-jardim.onrender.com/canteiros');
    const dados = await resposta.json();
    setSementes(dados.sementes);
  };

  useEffect(() => { carregarJardim(); }, []);

  const lidarComNovoPlantio = async (dadosSemente) => {
    const resposta = await fetch('https://api-jardim.onrender.com/plantar', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dadosSemente)
    });
    if (!resposta.ok) { alert("Semente já existe ou erro de formato!"); return; }
    setModalPlantarAberto(false);
    carregarJardim();
    reagirMascote(IconeMascotePlantar);
  };

  const abrirModalRega = (nomeSemente) => {
    setSementeSelecionada(nomeSemente);
    setModalRegaAberto(true);
  };

  const confirmarRega = async (nomeAntigo, novoNome) => {
    await fetch(`https://api-jardim.onrender.com/cuidar/${encodeURIComponent(nomeAntigo)}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ novo_nome: novoNome, regar: true })
    });
    setModalRegaAberto(false);
    carregarJardim();
    reagirMascote(IconeMascoteRegar);
  };

  const lidarComColheita = async (nomeSemente) => {
    await fetch(`https://api-jardim.onrender.com/cuidar/${encodeURIComponent(nomeSemente)}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ concluir: true })
    });
    carregarJardim();
    reagirMascote(IconeMascoteColher);
  };

  const abrirModalPoda = (nome) => {
    setSementeSelecionada(nome);
    if (exibindoCesto) {
      setModalExclusaoCestoAberto(true);
    } else {
      setModalPodarAberto(true);
    }
  };

  const confirmarExclusaoPermanenteCesto = async () => {
    try {
      const url = `https://api-jardim.onrender.com/podar/${encodeURIComponent(sementeSelecionada)}${googleToken ? `?token=${googleToken}` : ''}`;
      await fetch(url, {
        method: 'DELETE'
      });
      setModalExclusaoCestoAberto(false);
      carregarJardim();
      reagirMascote(IconeMascotePodar);
    } catch (erro) {
      console.error("Erro ao deletar permanentemente do cesto:", erro);
    }
  };

  const confirmarPoda = async (acao) => {
    if (acao === 'descartar') {
      const url = `https://api-jardim.onrender.com/podar/${encodeURIComponent(sementeSelecionada)}${googleToken ? `?token=${googleToken}` : ''}`;
      await fetch(url, { method: 'DELETE' });
      reagirMascote(IconeMascotePodar);
    } else if (acao === 'guardar') {
      const url = `https://api-jardim.onrender.com/cuidar/${encodeURIComponent(sementeSelecionada)}${googleToken ? `?token=${googleToken}` : ''}`;
      await fetch(url, {
        method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ cesto: true })
      });
      reagirMascote(IconeMascoteColher);
    }

    setModalPodarAberto(false);
    carregarJardim();
  };

  const tarefasVisiveis = sementes.filter(s => exibindoCesto ? s.cesto : !s.cesto);

  return (
      <div className="dashboard-container">

        <header className="box-painel header-jardim">
          <div className="header-conteudo">
            <img src={mascoteAtual} alt="Ícone Mascote" style={{ width: '8em', transition: 'all 0.3s ease' }} />
            <div className="header-textos">
              <h1>Meu Jardim</h1>
              <p>Bom dia, Jardineiro. O solo está fértil hoje!</p>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '60px' }}>

            {!googleToken ? (
                <button
                    type="button"
                    onClick={() => conectarGoogle()}
                    style={{
                      backgroundColor: 'transparent',
                      border: 'none',
                      color: 'var(--outline)',
                      fontSize: '12px',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '0',
                      fontFamily: 'inherit'
                    }}
                >
                  <img src={IconeCalendario} alt="Ícone Calendario" style={{ width: '18px'}}/>
                  <span style={{ textDecoration: 'underline' }}>Conectar Agenda</span>
                </button>
            ) : (
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <img src={IconeCalendario} alt="Ícone Calendario" style={{ width: '18px'}}/>
                  <span style={{ fontSize: '12px', color: 'var(--earth-brown)' }}>
                  Agenda Sincronizada
                </span>
                </div>
            )}

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                  className="btn"
                  style={{ backgroundColor: 'var(--white)', border: '2px solid var(--outline-light)', color: 'var(--earth-brown)' }}
                  onClick={() => setExibindoCesto(!exibindoCesto)}
              >
                {exibindoCesto ? 'Voltar ao Canteiro' : 'Ver Estufa'}
              </button>

              <button className="btn btn-primario" onClick={() => setModalPlantarAberto(true)}>
                Plantar
              </button>
            </div>

          </div>
        </header>

        <main className="box-painel">
          <div className="canteiro-top">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <img
                  src={exibindoCesto ? IconeEstufa : IconeCerca}
                  alt="Ícone da Seção"
                  style={{ width: '2.5em' }}
              />
              <h2>{exibindoCesto ? 'Estufa de Histórico' : 'Canteiro Principal'}</h2>
            </div>
            <span className="canteiro-contador">
              {tarefasVisiveis.length} {tarefasVisiveis.length === 1 ? 'Tarefa' : 'Tarefas'}
            </span>
          </div>

          <div className="grid-cards">
            {tarefasVisiveis.map((semente, index) => (
                <CardPlanta
                    key={index}
                    titulo={semente.nome}
                    descricao={semente.descricao}
                    contexto={semente.contexto}
                    dificuldade={semente.dificuldade}
                    prazo={semente.prazo}
                    concluido={semente.concluido}
                    historico={semente.historico}
                    isCesto={exibindoCesto}
                    onRegar={abrirModalRega}
                    onColher={lidarComColheita}
                    onPodar={abrirModalPoda}
                />
            ))}

            {tarefasVisiveis.length === 0 && (
                <p style={{ color: 'var(--outline)', fontStyle: 'italic', gridColumn: '1 / -1', textAlign: 'center', padding: '32px' }}>
                  {exibindoCesto ? 'Sua estufa está vazia.' : 'O canteiro está vazio. Plante uma semente!'}
                </p>
            )}
          </div>
        </main>

        {modalPlantarAberto && (
            <FormularioPlantar
                onPlantar={lidarComNovoPlantio}
                onFechar={() => setModalPlantarAberto(false)}
                googleToken={googleToken}
            />
        )}

        {modalRegaAberto && (
            <FormularioCuidar sementeAtual={sementeSelecionada} onSalvar={confirmarRega} onFechar={() => setModalRegaAberto(false)} />
        )}

        {modalPodarAberto && (
            <FormularioPodar sementeAtual={sementeSelecionada} onConfirmar={confirmarPoda} onFechar={() => setModalPodarAberto(false)} />
        )}

        {modalExclusaoCestoAberto && (
            <ConfirmacaoExclusaoModal
                nomeSemente={sementeSelecionada}
                onConfirmar={confirmarExclusaoPermanenteCesto}
                onFechar={() => setModalExclusaoCestoAberto(false)}
            />
        )}

      </div>
  );
}

export default App;