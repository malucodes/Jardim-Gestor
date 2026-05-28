import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

pool_conexoes = pooling.MySQLConnectionPool(
    pool_name="jardim_pool",
    pool_size=5,
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=4000,
    database="test",
    ssl_ca="",
    ssl_verify_cert=False,
    ssl_verify_identity=False
)

def conectar():
    return pool_conexoes.get_connection()

def listar_projetos(usuario_id):
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sementes WHERE usuario_id = %s", (usuario_id,))
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

def buscar_projeto(nome_projeto, usuario_id):
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sementes WHERE nome = %s AND usuario_id = %s", (nome_projeto, usuario_id))
    projeto = cursor.fetchone()
    db.close()
    return projeto

def adicionar_projeto(nome, descricao, contexto, dificuldade, prazo, usuario_id):
    db = conectar()
    cursor = db.cursor()
    sql = """INSERT INTO sementes (nome, descricao, contexto, dificuldade, prazo, usuario_id)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    valores = (nome, descricao, contexto, dificuldade, prazo, usuario_id)
    cursor.execute(sql, valores)
    db.commit()
    db.close()

def atualizar_projeto(nome_atual, usuario_id, novo_nome=None, regar=False, concluir=False, cesto=None):
    db = conectar()
    cursor = db.cursor()

    if novo_nome:
        cursor.execute("UPDATE sementes SET nome = %s WHERE nome = %s AND usuario_id = %s", (novo_nome, nome_atual, usuario_id))
        nome_atual = novo_nome

    if regar:
        cursor.execute("UPDATE sementes SET quantidade_regas = quantidade_regas + 1 WHERE nome = %s AND usuario_id = %s", (nome_atual, usuario_id))

    if concluir:
        cursor.execute("UPDATE sementes SET concluido = TRUE WHERE nome = %s AND usuario_id = %s", (nome_atual, usuario_id))

    if cesto is not None:
        cursor.execute("UPDATE sementes SET cesto = %s WHERE nome = %s AND usuario_id = %s", (cesto, nome_atual, usuario_id))

    db.commit()
    db.close()
    return True

def deletar_projeto(nome_projeto, usuario_id):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM sementes WHERE nome = %s AND usuario_id = %s", (nome_projeto, usuario_id))
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
      quantidade_regas INT DEFAULT 0,
      usuario_id VARCHAR(255) NOT NULL
      );
    """)

    try:
        cursor.execute("ALTER TABLE sementes ADD COLUMN usuario_id VARCHAR(255) DEFAULT 'jardineiro_anonimo'")
    except Exception:
        pass

    db.commit()
    db.close()
    print("🌱 Terreno do banco de dados com isolamento de usuários preparado com sucesso!")

inicializar_banco()