import datetime
import json

def carregar_dados(nome_arquivo):

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(lista_projetos, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(lista_projetos, arquivo, indent=4, ensure_ascii=False)

def buscar_projeto(lista_projetos, nome_busca):
    for projeto in lista_projetos:
        if projeto['nome'] == nome_busca:
            return projeto
    return None

def adicionar_projeto(lista_projetos, nome_projeto):

    novo_projeto = {
        "nome": nome_projeto,
        "concluido": False,
        "historico": []
    }
    lista_projetos.append(novo_projeto)
    return novo_projeto

def atualizar_projeto(lista_projetos, nome_busca, novo_nome=None, novo_status=None):

    projeto_encontrado = buscar_projeto(lista_projetos, nome_busca)

    if not projeto_encontrado:
        return False

    nome_final = novo_nome if novo_nome is not None else projeto_encontrado['nome']
    status_final = novo_status if novo_status is not None else projeto_encontrado['concluido']

    data_mudanca = datetime.datetime.now().strftime("%d-%m-%Y")

    if nome_final != projeto_encontrado['nome'] or status_final != projeto_encontrado['concluido']:
        registro = (data_mudanca, status_final, nome_final)
        projeto_encontrado['historico'].append(registro)

    projeto_encontrado['nome'] = nome_final
    projeto_encontrado['concluido'] = status_final

    return True

def deletar_projeto(lista_projetos, nome_busca):
    projeto_encontrado = buscar_projeto(lista_projetos, nome_busca)

    if projeto_encontrado:
        lista_projetos.remove(projeto_encontrado)
        return True
    return False