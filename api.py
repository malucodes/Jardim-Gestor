from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import jardim_core

app = FastAPI(title="Jardim-Gestor API")

# Configuração do CORS para permitir que o React/Front-end converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, colocamos a URL exata do front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# O arquivo de banco de dados
ARQUIVO_BD = "jardim.json"

# --- MODELOS DE DADOS (Como o React deve enviar os dados para o Python) ---
class SementeNova(BaseModel):
    nome: str

class SementeAtualizar(BaseModel):
    novo_nome: Optional[str] = None
    novo_status: Optional[bool] = None

# --- ROTAS DA API ---

@app.get("/canteiros")
def contemplar_jardim():
    """Retorna todas as sementes plantadas (O antigo 'Contemplar')"""
    canteiro = jardim_core.carregar_dados(ARQUIVO_BD)
    return {"sementes": canteiro}

@app.post("/plantar")
def plantar_semente(semente: SementeNova):
    """Adiciona uma nova semente ao jardim (O antigo 'Plantar')"""
    canteiro = jardim_core.carregar_dados(ARQUIVO_BD)

    # Verifica se já existe para não plantar duplicado
    if jardim_core.buscar_projeto(canteiro, semente.nome):
        raise HTTPException(status_code=400, detail="Essa semente já foi plantada!")

    nova_semente = jardim_core.adicionar_projeto(canteiro, semente.nome)
    jardim_core.salvar_dados(canteiro, ARQUIVO_BD)

    return {"mensagem": f"Semente '{semente.nome}' plantada com sucesso!", "dados": nova_semente}

@app.put("/cuidar/{nome_atual}")
def cuidar_semente(nome_atual: str, dados: SementeAtualizar):
    """Atualiza o nome ou status da semente (O antigo 'Cuidar')"""
    canteiro = jardim_core.carregar_dados(ARQUIVO_BD)

    sucesso = jardim_core.atualizar_projeto(
        canteiro,
        nome_atual,
        novo_nome=dados.novo_nome,
        novo_status=dados.novo_status
    )

    if not sucesso:
        raise HTTPException(status_code=404, detail="Semente não encontrada.")

    jardim_core.salvar_dados(canteiro, ARQUIVO_BD)
    return {"mensagem": f"Semente '{nome_atual}' cuidada com sucesso!"}

@app.delete("/podar/{nome}")
def podar_semente(nome: str):
    """Remove uma semente do jardim (O antigo 'Colher/Deletar')"""
    canteiro = jardim_core.carregar_dados(ARQUIVO_BD)

    sucesso = jardim_core.deletar_projeto(canteiro, nome)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Semente não encontrada.")

    jardim_core.salvar_dados(canteiro, ARQUIVO_BD)
    return {"mensagem": f"Semente '{nome}' podada do jardim."}