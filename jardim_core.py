import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (quando rodando no seu PC)
load_dotenv()

pool_conexoes = pooling.MySQLConnectionPool(
    pool_name="jardim_pool",
    pool_size=5,
    host=os.getenv("DB_HOST"),         # Puxa do cofre invisível!
    user=os.getenv("DB_USER"),         # Puxa do cofre invisível!
    password=os.getenv("DB_PASS"),
    port=4000,
    database="test",
    ssl_ca="",
    ssl_verify_cert=False,
    ssl_verify_identity=False
)
def conectar():
    return pool_conexoes.get_connection()

def listar_projetos():
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sementes")
    linhas = cursor.fetchall()
    db.close()

    sementes_formatadas = []
    for linha in linhas:
        sementes_formatadas.append({
            "nome": linha["nome"],
            "descricao": linha["descricao"],
            "contexto": linha["contexto"],
            "dificuldade": linha["dificuldade"],
            "prazo": linha["prazo"],
            "concluido": bool(linha["concluido"]),
            "cesto": bool(linha["cesto"]),
            "historico": ["Agua"] * linha["quantidade_regas"]
        })
    return sementes_formatadas

def buscar_projeto(nome_projeto):
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sementes WHERE nome = %s", (nome_projeto,))
    projeto = cursor.fetchone()
    db.close()
    return projeto

def adicionar_projeto(nome, descricao="", contexto="", dificuldade="", prazo=""):
    db = conectar()
    cursor = db.cursor()
    sql = """INSERT INTO sementes (nome, descricao, contexto, dificuldade, prazo)
             VALUES (%s, %s, %s, %s, %s)"""
    valores = (nome, descricao, contexto, dificuldade, prazo)
    cursor.execute(sql, valores)
    db.commit()
    db.close()

def atualizar_projeto(nome_atual, novo_nome=None, regar=False, concluir=False, cesto=None):
    db = conectar()
    cursor = db.cursor()

    if novo_nome:
        cursor.execute("UPDATE sementes SET nome = %s WHERE nome = %s", (novo_nome, nome_atual))
        nome_atual = novo_nome

    if regar:
        cursor.execute("UPDATE sementes SET quantidade_regas = quantidade_regas + 1 WHERE nome = %s", (nome_atual,))

    if concluir:
        cursor.execute("UPDATE sementes SET concluido = TRUE WHERE nome = %s", (nome_atual,))

    if cesto is not None:
        cursor.execute("UPDATE sementes SET cesto = %s WHERE nome = %s", (cesto, nome_atual))

    db.commit()
    db.close()
    return True

def deletar_projeto(nome_projeto):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM sementes WHERE nome = %s", (nome_projeto,))
    db.commit()
    db.close()
    return True

def inicializar_banco():
    db = conectar()
    cursor = db.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS sementes (
                                                           id INT AUTO_INCREMENT PRIMARY KEY,
                                                           nome VARCHAR(255) NOT NULL,
                       descricao TEXT,
                       contexto VARCHAR(100),
                       dificuldade VARCHAR(50),
                       prazo VARCHAR(100),
                       concluido BOOLEAN DEFAULT FALSE,
                       cesto BOOLEAN DEFAULT FALSE,
                       quantidade_regas INT DEFAULT 0
                       );
                   """)
    db.commit()
    db.close()
    print("🌱 Terreno do banco de dados e Pool de Conexões preparados com sucesso!")

inicializar_banco()