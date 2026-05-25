import React, { useState } from 'react';
import './App.css';
import IconeAgua from "./assets/agua.svg";

export default function FormularioCuidar({ sementeAtual, onSalvar, onFechar }) {
    const [novoNome, setNovoNome] = useState(sementeAtual);

    const enviarFormulario = (evento) => {
        evento.preventDefault();
        onSalvar(sementeAtual, novoNome);
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '400px' }}>
                <div className="modal-header">
                    <img src={IconeAgua} alt="Podar" style={{ width: '2em' }} />
                    <h2 style={{ color: 'var(--rain-blue)' }}>
                        Regando Semente...
                    </h2>
                    <button type="button" className="btn-fechar-modal" onClick={onFechar}>&times;</button>
                </div>

                <form onSubmit={enviarFormulario}>
                    <div className="modal-body">
                        <p style={{ fontSize: '14px', color: 'var(--muted-green)' }}>
                            Ao regar, a sua planta crescerá um estágio. Você também pode renomear a tarefa se precisar.
                        </p>

                        <div className="grupo-campo">
                            <label>Nome da Tarefa</label>
                            <input
                                type="text"
                                className="campo-input"
                                value={novoNome}
                                onChange={(e) => setNovoNome(e.target.value)}
                                autoFocus
                            />
                        </div>
                    </div>

                    <div className="modal-footer">
                        <button type="button" className="btn" style={{ border: 'none', color: 'var(--outline)' }} onClick={onFechar}>
                            Cancelar
                        </button>
                        <button type="submit" className="btn btn-secundario">
                            <img src={IconeAgua} alt="Podar" style={{ width: '20px' }} /> Confirmar Rega
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}