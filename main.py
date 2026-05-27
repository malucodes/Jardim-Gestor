import uvicorn
from datetime import datetime
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

def deletar_tarefa_google(nome_tarefa: str, token: str):
    url_listar = "https://tasks.googleapis.com/tasks/v1/lists/@default/tasks"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resposta = requests.get(url_listar, headers=headers, timeout=5)
        if resposta.status_code == 200:
            tarefas = resposta.json().get("items", [])

            for tarefa in tarefas:
                if tarefa.get("title") == nome_tarefa:
                    id_tarefa = tarefa.get("id")
                    url_deletar = f"https://tasks.googleapis.com/tasks/v1/lists/@default/tasks/{id_tarefa}"

                    requests.delete(url_deletar, headers=headers, timeout=5)
                    print(f"✅ Tarefa '{nome_tarefa}' deletada do Google Tasks!")
                    break
    except Exception as e:
        print(f"Erro ao deletar no Google Tasks: {e}")
# -------------------------------------------------------

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

        prazo_final = f"{semente.prazo.strip()}T00:00:00.000Z"

        dados_tarefa = {
            "title": semente.nome,
            "notes": semente.descricao,
            "due": prazo_final
        }

        try:
            requests.post(url_google, headers=headers, json=dados_tarefa, timeout=5)
            print(f"✅ Tarefa '{semente.nome}' criada no Google Tasks!")
        except Exception as e:
            print(f"Erro ao enviar para o Google: {e}")
    # ------------------------------------------

    return {"mensagem": "Plantada na nuvem!"}

@app.put("/cuidar/{nome_atual}")
def cuidar_semente(nome_atual: str, dados: SementeAtualizar, token: Optional[str] = None):
    jardim_core.atualizar_projeto(
        nome_atual,
        novo_nome=dados.novo_nome,
        regar=dados.regar,
        concluir=dados.concluir,
        cesto=dados.cesto
    )

    if dados.cesto and token:
        deletar_tarefa_google(nome_atual, token)

    return {"mensagem": "Cuidada com sucesso!"}

@app.delete("/podar/{nome}")
def podar_semente(nome: str, token: Optional[str] = None):
    jardim_core.deletar_projeto(nome)

    if token:
        deletar_tarefa_google(nome, token)

    return {"mensagem": f"Semente '{nome}' podada com sucesso."}

if __name__ == "__main__":
    print("=========================================================")
    print("☁️ Conectando ao Banco de Dados na Nuvem...")
    print("O Jardim está no ar em: http://localhost:8000/docs")
    print("=========================================================")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)