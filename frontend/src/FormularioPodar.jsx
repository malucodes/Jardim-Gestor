import React from 'react';
import './App.css';
import IconePodarTesoura from "./assets/podar_excluir.svg";
import IconeEstufa from "./assets/estufa.svg"
import IconeLixeira from "./assets/lixeira.svg"

export default function FormularioPodar({ sementeAtual, onConfirmar, onFechar }) {
    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '420px' }}>
                <div className="modal-header">
                    <img src={IconePodarTesoura} alt="Podar" style={{ width: '2em' }} />
                    <h2 style={{ color: 'var(--earth-brown)' }}>
                        Podando Semente...
                    </h2>
                    <button type="button" className="btn-fechar-modal" onClick={onFechar}>&times;</button>
                </div>

                <div className="modal-body">
                    <p style={{ fontSize: '15px', color: 'var(--muted-green)', margin: '0 0 16px 0', lineHeight: '1.5' }}>
                        O que você deseja fazer com a tarefa <strong>"{sementeAtual}"</strong>?
                    </p>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <button
                            className="btn btn-secundario"
                            style={{ width: '100%', justifyContent: 'center' }}
                            onClick={() => onConfirmar('guardar')}
                        >
                            <img src={IconeEstufa} alt="Podar" style={{ width: '20px' }} /> Guardar na Estufa (Histórico)
                        </button>

                        <button
                            className="btn btn-perigo"
                            style={{ width: '100%', justifyContent: 'center' }}
                            onClick={() => onConfirmar('descartar')}
                        >
                            <img src={IconeLixeira} alt="Podar" style={{ width: '20px' }} /> Descartar Permanentemente
                        </button>
                    </div>
                </div>

                <div className="modal-footer">
                    <button type="button" className="btn" style={{ border: 'none', color: 'var(--outline)' }} onClick={onFechar}>
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    );
}