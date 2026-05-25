import { useState } from 'react';
import IconeBroto from './assets/broto_em_andamento.svg'
import './App.css';

export default function FormularioPlantar({ onPlantar, onFechar, googleToken }) {
    const [nome, setNome] = useState('');
    const [descricao, setDescricao] = useState('');
    const [prazo, setPrazo] = useState('');
    const [notas, setNotas] = useState('');
    const [contextoSelecionado, setContextoSelecionado] = useState('');
    const [dificuldadeSelecionada, setDificuldadeSelecionada] = useState('');

    const contextos = ['Casa', 'Trabalho', 'Estudos', 'Viagem', 'Online'];
    const dificuldades = ['Fácil', 'Médio', 'Difícil', 'Épico'];

    const enviarFormulario = (evento) => {
        evento.preventDefault();
        if (!nome.trim()) return;

        onPlantar({
            nome,
            descricao,
            prazo,
            notas,
            contexto: contextoSelecionado,
            dificuldade: dificuldadeSelecionada,
            google_token: googleToken
        });

        setNome('');
        setDescricao('');
        setPrazo('');
        setNotas('');
        setContextoSelecionado('');
        setDificuldadeSelecionada('');
    };

    const obterClasseDificuldade = (nivel, selecionado) => {
        let classeBase = "chip ";
        if (nivel === 'Fácil' || nivel === 'Épico') classeBase += "chip-dificuldade";
        else if (nivel === 'Médio') classeBase += "chip-status";
        else if (nivel === 'Difícil') classeBase += "chip-perigo";

        return selecionado ? `${classeBase} chip-ativo` : classeBase;
    };


    return (
        <div className="modal-overlay">
            <div className="modal-content modal-scroll">

                <div className="modal-header">
                    <img src={IconeBroto} alt="Ícone Broto" style={{ width: '2em'}} />
                    <h2>Plantando semente...</h2>
                    <button type="button" className="btn-fechar-modal" onClick={onFechar}>&times;</button>
                </div>

                <form onSubmit={enviarFormulario}>
                    <div className="modal-body" style={{ maxHeight: '65vh', overflowY: 'auto' }}>

                        <div className="grupo-campo">
                            <label htmlFor="nome-tarefa">Nome da Tarefa</label>
                            <input
                                id="nome-tarefa"
                                type="text"
                                className="campo-input"
                                placeholder="Ex.: Ler 20 páginas..."
                                value={nome}
                                onChange={(e) => setNome(e.target.value)}
                                required
                                autoFocus
                            />
                        </div>

                        <div className="grupo-campo">
                            <label htmlFor="descricao-tarefa">Descrição</label>
                            <textarea
                                id="descricao-tarefa"
                                className="campo-textarea"
                                placeholder="Detalhes sobre a planta..."
                                value={descricao}
                                onChange={(e) => setDescricao(e.target.value)}
                                rows="2"
                            />
                        </div>

                        <div className="grupo-campo">
                            <label htmlFor="prazo-tarefa">Prazo</label>
                            <input
                                id="prazo-tarefa"
                                type="date"
                                className="campo-input"
                                value={prazo}
                                onChange={(e) => setPrazo(e.target.value)}
                                required
                            />
                        </div>

                        <div className="grupo-campo">
                            <label htmlFor="notas-tarefa">Notas</label>
                            <textarea
                                id="notas-tarefa"
                                className="campo-textarea"
                                placeholder="Anote aqui observações sobre o crescimento..."
                                value={notas}
                                onChange={(e) => setNotas(e.target.value)}
                                rows="3"
                            />
                        </div>

                        <hr style={{ border: 'none', borderTop: '1px solid var(--outline-light)', margin: '16px 0' }} />

                        <div className="grupo-campo">
                            <label style={{ textTransform: 'uppercase', fontSize: '12px', letterSpacing: '0.05em' }}>
                                Ambiente / Contexto
                            </label>
                            <div className="chips-container">
                                {contextos.map(ctx => (
                                    <span
                                        key={ctx}
                                        onClick={() => setContextoSelecionado(ctx)}
                                        className={`chip chip-contexto ${contextoSelecionado === ctx ? 'chip-ativo' : ''}`}
                                        style={{ cursor: 'pointer', transition: 'all 0.2s ease' }}
                                    >
                                        {ctx}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div className="grupo-campo" style={{ marginTop: '8px' }}>
                            <label style={{ textTransform: 'uppercase', fontSize: '12px', letterSpacing: '0.05em' }}>
                                Nutrientes / Dificuldade
                            </label>
                            <div className="chips-container">
                                {dificuldades.map(dif => (
                                    <span
                                        key={dif}
                                        onClick={() => setDificuldadeSelecionada(dif)}
                                        className={obterClasseDificuldade(dif, dificuldadeSelecionada === dif)}
                                        style={{ cursor: 'pointer', transition: 'all 0.2s ease' }}
                                    >
                                        {dif}
                                    </span>
                                ))}
                            </div>
                        </div>

                    </div>

                    <div className="modal-footer">
                        <button type="button" className="btn" style={{ backgroundColor: 'transparent', border: 'none', color: 'var(--outline)' }} onClick={onFechar}>
                            Cancelar
                        </button>
                        <button type="submit" className="btn btn-primario">
                            Plantar Semente
                        </button>
                    </div>
                </form>

            </div>
        </div>
    );
}