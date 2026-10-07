import json
import os
from datetime import datetime

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CHAMADOS = "chamados.json"

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def inicializar_usuarios():
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    if not usuarios:
        usuarios = [
            {"usuario": "cliente1", "senha": "123", "nome": "João Cliente", "tipo": "cliente"},
            {"usuario": "tecnico1", "senha": "123", "nome": "Maria Técnica", "tipo": "tecnico"}
        ]
        salvar_dados(ARQUIVO_USUARIOS, usuarios)
    return usuarios

def login():
    usuarios = inicializar_usuarios()
    print("\n=== SISTEMA DE HELP DESK - InovaTech ===")
    print("Login")
    user = input("Usuário: ").strip()
    senha = input("Senha: ").strip()
    for u in usuarios:
        if u["usuario"] == user and u["senha"] == senha:
            print(f"\nBem-vindo(a), {u['nome']}!")
            return u
    print("Usuário ou senha inválidos.")
    return None

def gerar_id(chamados):
    if not chamados:
        return 1
    return max(c["id"] for c in chamados) + 1

def abrir_chamado(usuario_logado):
    chamados = carregar_dados(ARQUIVO_CHAMADOS)
    print("\n=== ABRIR NOVO CHAMADO ===")
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    
    print("Categorias: 1-Hardware | 2-Software | 3-Rede | 4-Outros")
    cat = input("Escolha a categoria: ").strip()
    categorias = {"1": "Hardware", "2": "Software", "3": "Rede", "4": "Outros"}
    categoria = categorias.get(cat, "Outros")
    
    print("Prioridade: 1-Baixa | 2-Média | 3-Alta | 4-Crítica")
    pri = input("Escolha a prioridade: ").strip()
    prioridades = {"1": "Baixa", "2": "Média", "3": "Alta", "4": "Crítica"}
    prioridade = prioridades.get(pri, "Média")
    
    novo = {
        "id": gerar_id(chamados),
        "titulo": titulo,
        "descricao": descricao,
        "categoria": categoria,
        "prioridade": prioridade,
        "status": "Aberto",
        "solicitante": usuario_logado["usuario"],
        "tecnico": None,
        "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    chamados.append(novo)
    salvar_dados(ARQUIVO_CHAMADOS, chamados)
    print(f"\nChamado #{novo['id']} aberto com sucesso!")

def listar_chamados(usuario_logado, todos=False):
    chamados = carregar_dados(ARQUIVO_CHAMADOS)
    print("\n=== LISTA DE CHAMADOS ===")
    if not chamados:
        print("Nenhum chamado registrado.")
        return
    for c in chamados:
        if todos or c["solicitante"] == usuario_logado["usuario"] or usuario_logado["tipo"] == "tecnico":
            print(f"\nID: {c['id']} | Status: {c['status']} | Prioridade: {c['prioridade']}")
            print(f"Título: {c['titulo']}")
            print(f"Categoria: {c['categoria']} | Solicitante: {c['solicitante']}")
            print(f"Técnico: {c['tecnico'] or 'Não atribuído'}")
            print(f"Abertura: {c['data_abertura']}")

def buscar_chamado():
    chamados = carregar_dados(ARQUIVO_CHAMADOS)
    try:
        id_busca = int(input("\nDigite o ID do chamado: "))
    except ValueError:
        print("ID inválido.")
        return
    for c in chamados:
        if c["id"] == id_busca:
            print(f"\n=== CHAMADO #{c['id']} ===")
            print(f"Título: {c['titulo']}")
            print(f"Descrição: {c['descricao']}")
            print(f"Categoria: {c['categoria']} | Prioridade: {c['prioridade']}")
            print(f"Status: {c['status']}")
            print(f"Solicitante: {c['solicitante']} | Técnico: {c['tecnico'] or 'Não atribuído'}")
            print(f"Abertura: {c['data_abertura']} | Atualização: {c['data_atualizacao']}")
            return
    print("Chamado não encontrado.")

def atualizar_status(usuario_logado):
    if usuario_logado["tipo"] != "tecnico":
        print("Apenas técnicos podem atualizar status.")
        return
    chamados = carregar_dados(ARQUIVO_CHAMADOS)
    try:
        id_chamado = int(input("\nID do chamado: "))
    except ValueError:
        print("ID inválido.")
        return
    for c in chamados:
        if c["id"] == id_chamado:
            print("Status: 1-Aberto | 2-Em andamento | 3-Resolvido | 4-Fechado")
            op = input("Novo status: ").strip()
            status_map = {"1": "Aberto", "2": "Em andamento", "3": "Resolvido", "4": "Fechado"}
            if op in status_map:
                c["status"] = status_map[op]
                c["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                salvar_dados(ARQUIVO_CHAMADOS, chamados)
                print("Status atualizado com sucesso!")
            else:
                print("Opção inválida.")
            return
    print("Chamado não encontrado.")

def atribuir_tecnico(usuario_logado):
    if usuario_logado["tipo"] != "tecnico":
        print("Apenas técnicos podem atribuir responsáveis.")
        return
    chamados = carregar_dados(ARQUIVO_CHAMADOS)
    try:
        id_chamado = int(input("\nID do chamado: "))
    except ValueError:
        print("ID inválido.")
        return
    for c in chamados:
        if c["id"] == id_chamado:
            c["tecnico"] = usuario_logado["usuario"]
            c["status"] = "Em andamento"
            c["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            salvar_dados(ARQUIVO_CHAMADOS, chamados)
            print(f"Chamado #{id_chamado} atribuído a {usuario_logado['nome']}.")
            return
    print("Chamado não encontrado.")

def menu(usuario_logado):
    while True:
        print("\n========== MENU PRINCIPAL ==========")
        print("1 - Abrir chamado")
        print("2 - Listar meus chamados")
        if usuario_logado["tipo"] == "tecnico":
            print("3 - Listar todos os chamados")
            print("4 - Buscar chamado por ID")
            print("5 - Atualizar status")
            print("6 - Atribuir chamado a mim")
            print("0 - Sair")
        else:
            print("3 - Buscar chamado por ID")
            print("0 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            abrir_chamado(usuario_logado)
        elif opcao == "2":
            listar_chamados(usuario_logado, todos=False)
        elif opcao == "3":
            if usuario_logado["tipo"] == "tecnico":
                listar_chamados(usuario_logado, todos=True)
            else:
                buscar_chamado()
        elif opcao == "4" and usuario_logado["tipo"] == "tecnico":
            buscar_chamado()
        elif opcao == "5" and usuario_logado["tipo"] == "tecnico":
            atualizar_status(usuario_logado)
        elif opcao == "6" and usuario_logado["tipo"] == "tecnico":
            atribuir_tecnico(usuario_logado)
        elif opcao == "0":
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida.")

def main():
    usuario = None
    while usuario is None:
        usuario = login()
    menu(usuario)

if __name__ == "__main__":
    main()
