import React from 'react';
import IconeLixeira from "./assets/lixeira.svg"
import './App.css';

export default function ConfirmacaoExclusaoModal({ nomeSemente, onConfirmar, onFechar }) {
    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '500px' }}>
                <div className="modal-header">
                    <img src={IconeLixeira} alt="Podar" style={{ width: '2em' }} />
                    <h2 style={{ color: 'var(--floral-coral)' }}>
                        Confirmando Exclusão...
                    </h2>
                    <button type="button" className="btn-fechar-modal" onClick={onFechar}>&times;</button>
                </div>

                <div className="modal-body" style={{ textAlign: 'center', padding: '24px 16px' }}>
                    <p style={{ fontSize: '18px', fontWeight: '600', color: 'var(--floral-coral)'}}>
                        Atenção: Esta ação é irreversível!
                    </p>

                    <p style={{ fontSize: '15px', color: 'var(--muted-green)', lineHeight: '1.5' }}>
                        Deseja apagar permanentemente a tarefa<br/>
                        <strong>"{nomeSemente}"</strong>?
                    </p>
                </div>

                <div className="modal-footer" style={{ justifyContent: 'center', gap: '16px' }}>
                    <button type="button" className="btn" style={{ backgroundColor: 'var(--white)', border: '1px solid var(--outline)', padding: '5px 10px' }} onClick={onFechar}>
                        Cancelar
                    </button>
                    <button type="button" className="btn btn-perigo" style={{ padding: '10px 24px' }} onClick={onConfirmar}>
                        Deletar Permanentemente
                    </button>
                </div>
            </div>
        </div>
    );
}