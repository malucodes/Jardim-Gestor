import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import jardim_core

app = FastAPI(
    title="O Jardim - API",
    description="Motor de gestão de atividades e canteiros metafóricos rodando na Nuvem.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SementeNova(BaseModel):
    nome: str
    descricao: Optional[str] = "Cuidando desta semente no jardim."
    contexto: Optional[str] = "Geral"
    dificuldade: Optional[str] = "Normal"
    prazo: Optional[str] = "-"

class SementeAtualizar(BaseModel):
    novo_nome: Optional[str] = None
    regar: Optional[bool] = False
    concluir: Optional[bool] = False
    cesto: Optional[bool] = None

@app.get("/canteiros")
def contemplar_jardim():
    # Puxa tudo direto do banco de dados na nuvem
    canteiro = jardim_core.listar_projetos()
    return {"sementes": canteiro}

@app.post("/plantar")
def plantar_semente(semente: SementeNova):
    if jardim_core.buscar_projeto(semente.nome):
        raise HTTPException(status_code=400, detail="Essa semente já está no solo!")

    jardim_core.adicionar_projeto(
        semente.nome, semente.descricao, semente.contexto, semente.dificuldade, semente.prazo
    )
    return {"mensagem": "Plantada na nuvem!"}

@app.put("/cuidar/{nome_atual}")
def cuidar_semente(nome_atual: str, dados: SementeAtualizar):
    jardim_core.atualizar_projeto(
        nome_atual,
        novo_nome=dados.novo_nome,
        regar=dados.regar,
        concluir=dados.concluir,
        cesto=dados.cesto
    )
    return {"mensagem": "Cuidada com sucesso!"}

@app.delete("/podar/{nome}")
def podar_semente(nome: str):
    jardim_core.deletar_projeto(nome)
    return {"mensagem": f"Semente '{nome}' podada com sucesso."}

if __name__ == "__main__":
    print("=========================================================")
    print("☁️ Conectando ao Banco de Dados na Nuvem...")
    print("O Jardim está no ar em: http://localhost:8000/docs")
    print("=========================================================")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)