import React from 'react';

import IconeSemente from './assets/semente_nova.svg';
import IconeBroto from './assets/broto_em_andamento.svg';
import IconeMuda from './assets/planta_frequente.svg';
import IconeArvore from './assets/arvore_muito_produtiva.svg';
import IconeColheita from './assets/colher_contemplar.svg';

import IconeRegaDrop from './assets/agua.svg';
import IconeColherTrigo from './assets/colher_contemplar.svg';
import IconePodarTesoura from './assets/podar_excluir.svg';
import IconeLixeira from "./assets/lixeira.svg"

export default function CardPlanta({
                                       titulo,
                                       descricao = "Cuidando desta semente no jardim.",
                                       contexto = "Casa",
                                       dificuldade = "Fácil",
                                       prazo = "3 dias",
                                       concluido,
                                       historico,
                                       isCesto,
                                       onRegar,
                                       onColher,
                                       onPodar
                                   }) {

    const quantidadeRegas = historico ? historico.length : 0;

    let progresso = 15;
    let estagioNome = "Semente";
    let estagioSub = "Escrevendo";
    let iconeFase = IconeSemente;

    // --- NOVA LÓGICA DE MATURIDADE ---
    if (concluido) {
        progresso = 100;
        estagioNome = "Colheita";
        estagioSub = "Concluída!";
        iconeFase = IconeColheita;
    } else if (quantidadeRegas >= 4) {
        // Atingiu 100% de regas: Pronta para colher!
        progresso = 100;
        estagioNome = "Madura";
        estagioSub = "Pronta para colher";
        iconeFase = IconeArvore;
    } else if (quantidadeRegas === 3) {
        // Estágio de 85%: O botão de regar ainda aparece aqui
        progresso = 85;
        estagioNome = "Árvore";
        estagioSub = "Quase pronta";
        iconeFase = IconeArvore;
    } else if (quantidadeRegas === 2) {
        progresso = 62;
        estagioNome = "Muda";
        estagioSub = "Metade do caminho";
        iconeFase = IconeMuda;
    } else if (quantidadeRegas === 1) {
        progresso = 38;
        estagioNome = "Broto";
        estagioSub = "Em andamento";
        iconeFase = IconeBroto;
    }

    return (
        <div className="card-planta">
            <div className="card-header-horizontal">
                <div className="card-icone-quadrado">
                    <img src={iconeFase} alt={`Estágio: ${estagioNome}`} style={{ width: '32px' }} />
                </div>
                <div className="card-textos-header">
                    <h2 style={{ textDecoration: concluido ? 'line-through' : 'none' }}>
                        {titulo}
                    </h2>
                    <p>{descricao}</p>
                </div>
            </div>

            <div className="chips-container" style={{ margin: '4px 0' }}>
                <span className="chip chip-contexto">{contexto || "Geral"}</span>
                <span className="chip chip-dificuldade">{dificuldade || "Normal"}</span>
                <span className="chip chip-status">{isCesto ? "Concluído" : (prazo || "-")}</span>
            </div>

            <div className="progresso-container">
                <div className="progresso-header">
                    <span className="progresso-texto">Crescimento</span>
                    <span className="progresso-valor">{progresso}%</span>
                </div>
                <div className="progresso-cocho">
                    <div
                        className="progresso-preenchimento"
                        style={{ width: `${progresso}%` }}
                    ></div>
                </div>
            </div>

            <div className="card-acoes-nova">
                {isCesto ? (
                    <button
                        className="btn btn-perigo btn-icon-only"
                        style={{ marginLeft: 'auto' }}
                        onClick={() => onPodar(titulo)}
                    >
                        <img src={IconeLixeira} alt="Deletar Permanentemente" style={{ width: '18px' }} />
                    </button>
                ) : (
                    <>
                        {/* MAGIA AQUI: O botão Regar só é desenhado na tela se o progresso for menor que 100 */}
                        {progresso < 100 && (
                            <button
                                className="btn btn-secundario"
                                style={{ flex: 1, opacity: concluido ? 0.5 : 1, pointerEvents: concluido ? 'none' : 'auto' }}
                                onClick={() => onRegar(titulo)}
                            >
                                <img src={IconeRegaDrop} alt="" style={{ width: '16px' }} />
                                REGAR
                            </button>
                        )}

                        <button
                            className="btn btn-primario"
                            style={{ flex: 1, opacity: concluido ? 0.5 : 1, pointerEvents: concluido ? 'none' : 'auto' }}
                            onClick={() => onColher(titulo)}
                        >
                            <img src={IconeColherTrigo} alt="" style={{ width: '16px' }} />
                            COLHER
                        </button>

                        <button className="btn btn-perigo btn-icon-only" onClick={() => onPodar(titulo)}>
                            <img src={IconePodarTesoura} alt="Podar" style={{ width: '18px' }} />
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}