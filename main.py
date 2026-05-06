import datetime
import json

def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"\n[!] AVISO: O arquivo '{nome_arquivo}' está corrompido ou vazio.")
        print("Iniciando com um Jardim limpo (lista vazia).")
        return []

def salvar_dados(lista_projetos, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(lista_projetos, arquivo, indent=4, ensure_ascii=False)

def buscar_projeto(lista_projetos, nome_busca):
    for projeto in lista_projetos:
        if projeto['nome'] == nome_busca:
            return projeto
    return None

def adicionar_projeto(lista_projetos):
    print("=========================================================")
    print("\nPreparando a terra...")

    try:
        quantidade_projetos = int(input("Quantas sementes deseja adicionar? "))

        if quantidade_projetos <= 0:
            print("\nQuantidade Inválida de Sementes! (Deve ser maior que zero).")
            print("Tente novamente.")
        else:
            for projeto in range(quantidade_projetos):
                nome_projeto = input("Digite o nome da semente: ")

                novo_projeto = {
                    "nome": nome_projeto,
                    "concluido": False,
                    "historico": []
                }
                lista_projetos.append(novo_projeto)

                print(f"Semente \"{nome_projeto}\" plantada com sucesso no seu Jardim!")
                print("Dica: Lembre-se de regá-las periodicamente nos próximos dias.")

    except ValueError:
        print("\nERRO: Formato inválido. Por favor, digite apenas números inteiros (ex: 1, 2, 3).")

    print("=========================================================")

def listar_projetos(lista_projetos):
    print("=========================================================")
    print("\nAbrindo os portões do seu Jardim...\n")

    if len(lista_projetos) == 0:
        print("O solo está descansando. Não há nenhuma semente plantada no momento.")
    else:
        print("[ Sementes em Cultivo ]")
        for i, projeto in enumerate(lista_projetos):
            status = "Concluído" if projeto["concluido"] else "Em andamento"
            print(f"\n 🌱 Semente {i+1}: {projeto['nome']}")
            print(f"    Status: {status}")

            if projeto["historico"]:
                print("    > Histórico de Mudanças:")
                for registro in projeto["historico"]:
                    print(f"      No dia [{registro[0]}] o nome foi alterado para '{registro[2]}'. Status: {registro[1]}")

        print("\nO solo está fértil hoje. O que vamos regar?")
    print("=========================================================")

def atualizar_projeto(lista_projetos):
    print("=========================================================")
    print("\nPegando o regador...")
    nome_busca = input("Qual semente você deseja cuidar/editar? ")

    projeto_encontrado = buscar_projeto(lista_projetos, nome_busca)

    if projeto_encontrado is not None:
        print(f"\nCuidando da semente: {projeto_encontrado['nome']}")

        novo_nome = input("Digite o novo nome (ou pressione Enter para manter o mesmo): ")
        if novo_nome == "":
            novo_nome = projeto_encontrado['nome']

        novo_status_str = input("Esta semente já brotou? (s/n): ").strip().lower()
        novo_status = True if novo_status_str == 's' else False

        data_mudanca = datetime.datetime.now().strftime("%d-%m-%Y")

        registro = (data_mudanca, novo_status, novo_nome)
        projeto_encontrado['historico'].append(registro)

        projeto_encontrado['nome'] = novo_nome
        projeto_encontrado['concluido'] = novo_status

        print("\nSemente cuidada (atualizada) com sucesso!")
    else:
        print(f"A semente '{nome_busca}' não foi encontrada no seu Jardim.")
    print("=========================================================")

def deletar_projeto(lista_projetos):
    print("=========================================================")
    print("\nPegando a tesoura de poda...")
    nome_busca = input("Qual semente você deseja podar/remover? ")

    projeto_encontrado = buscar_projeto(lista_projetos, nome_busca)

    if projeto_encontrado is not None:
        lista_projetos.remove(projeto_encontrado)
        print(f"\nA semente '{nome_busca}' foi podada com sucesso e removida do Jardim.")
    else:
        print(f"A semente '{nome_busca}' não foi encontrada.")
    print("=========================================================")

def mostrar_sobre():
    print("=========================================================")
    print("[ O JARDIM ]")
    print("Software feito por Maria Luiza")
    print("=========================================================")

arquivo_bd = "jardim.json"
canteiro_de_sementes = carregar_dados(arquivo_bd)

while True:
    print("\n=========================================================")
    print("[ O JARDIM ]")
    print("O que você deseja fazer hoje?")
    print("[1] Plantar    (Adicionar novo projeto)")
    print("[2] Contemplar (Ver meus canteiros e status)")
    print("[3] Cuidar     (Regar progresso ou editar projetos)")
    print("[4] Colher     (Finalizar ou podar projetos antigos)")
    print("[5] Sobre")
    print("[6] Sair")
    print("=========================================================")
    comando = input("> Digite sua escolha (1-6): ")

    if comando == "1":
        adicionar_projeto(canteiro_de_sementes)
    elif comando == "2":
        listar_projetos(canteiro_de_sementes)
    elif comando == "3":
        atualizar_projeto(canteiro_de_sementes)
    elif comando == "4":
        deletar_projeto(canteiro_de_sementes)
    elif comando == "5":
        mostrar_sobre()
    elif comando == "6":
        salvar_dados(canteiro_de_sementes, arquivo_bd)

        print("=========================================================")
        print("[ O JARDIM ]")
        print("\nFechando os portões do Jardim...")
        print("Progresso salvo com sucesso!")
        print("Você fez o que pôde por hoje. Descanse a mente e volte quando tiver energia.")
        print("Até logo!")
        print("=========================================================")
        break
    else:
        print("=========================================================")
        print("[ O JARDIM ]")
        print("\nVento forte! Opção inválida. Tente escolher um número de 1 a 6.")
        input("\nPressione [ENTER] para tentar novamente...")