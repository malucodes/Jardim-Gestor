import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import jardim_core

app = FastAPI(
    title="O Jardim - API",
    description="Motor de gestão de atividades e canteiros metafóricos rodando na Nuvem.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ciberjardim.vercel.app"
    ],
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
    google_token: Optional[str] = None

class SementeAtualizar(BaseModel):
    novo_nome: Optional[str] = None
    regar: Optional[bool] = False
    concluir: Optional[bool] = False
    cesto: Optional[bool] = None

@app.get("/canteiros")
def contemplar_jardim():
    canteiro = jardim_core.listar_projetos()
    return {"sementes": canteiro}

@app.post("/plantar")
def plantar_semente(semente: SementeNova):
    if jardim_core.buscar_projeto(semente.nome):
        raise HTTPException(status_code=400, detail="Essa semente já está no solo!")

    jardim_core.adicionar_projeto(
        semente.nome, semente.descricao, semente.contexto, semente.dificuldade, semente.prazo
    )

    if semente.google_token and semente.prazo and semente.prazo != "-":
        url_google = "https://tasks.googleapis.com/tasks/v1/lists/@default/tasks"

        headers = {
            "Authorization": f"Bearer {semente.google_token}",
            "Content-Type": "application/json"
        }

        data_formatada = f"{semente.prazo}T12:00:00.000Z"

        dados_tarefa = {
            "title": semente.nome,
            "notes": semente.descricao,
            "due": data_formatada
        }

        try:
            resposta_google = requests.post(url_google, headers=headers, json=dados_tarefa, timeout=5)

            if resposta_google.status_code == 200:
                print("✅ Tarefa criada com sucesso no Google Tasks!")
            else:
                print(f"⚠️ Erro do Google: {resposta_google.text}")

        except Exception as e:
            print(f"Erro de conexão com o Google: {e}")
    # ---------------------------------------------------------

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