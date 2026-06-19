from auth import fazer_login, fazer_logout
from quartos import adicionar_quarto, listar_quartos, editar_quarto, remover_quarto, consultar_disponibilidade
from clientes import registar_cliente, listar_clientes, procurar_cliente, historico_cliente
from reservas import fazer_reserva, cancelar_reserva, listar_reservas
from checkinout import fazer_checkin, fazer_checkout
from relatorios import relatorio_ocupacao

def menu_quartos():
    while True:
        print("\n--- QUARTOS ---")
        print("1. Listar quartos")
        print("2. Adicionar quarto")
        print("3. Editar quarto")
        print("4. Remover quarto")
        print("5. Consultar disponibilidade")
        print("0. Voltar")
        opcao = input("Opção: ")
        if opcao == "1": listar_quartos()
        elif opcao == "2": adicionar_quarto()
        elif opcao == "3": editar_quarto()
        elif opcao == "4": remover_quarto()
        elif opcao == "5": consultar_disponibilidade()
        elif opcao == "0": break
        else: print("Opção inválida.")

def menu_clientes():
    while True:
        print("\n--- CLIENTES ---")
        print("1. Listar clientes")
        print("2. Registar cliente")
        print("3. Procurar cliente")
        print("4. Histórico de reservas")
        print("0. Voltar")
        opcao = input("Opção: ")
        if opcao == "1": listar_clientes()
        elif opcao == "2": registar_cliente()
        elif opcao == "3": procurar_cliente()
        elif opcao == "4": historico_cliente()
        elif opcao == "0": break
        else: print("Opção inválida.")

def menu_reservas():
    while True:
        print("\n--- RESERVAS ---")
        print("1. Listar reservas")
        print("2. Efectuar reserva")
        print("3. Cancelar reserva")
        print("4. Check-in")
        print("5. Check-out")
        print("0. Voltar")
        opcao = input("Opção: ")
        if opcao == "1": listar_reservas()
        elif opcao == "2": fazer_reserva()
        elif opcao == "3": cancelar_reserva()
        elif opcao == "4": fazer_checkin()
        elif opcao == "5": fazer_checkout()
        elif opcao == "0": break
        else: print("Opção inválida.")

def menu_principal(utilizador):
    while True:
        print(f"\n=============================")
        print(f"  HOTEL - Sistema de Gestão")
        print(f"  Utilizador: {utilizador['nome']} ({utilizador['perfil']})")
        print(f"=============================")
        print("1. Quartos")
        print("2. Clientes")
        print("3. Reservas")
        print("4. Relatório de ocupação")
        print("0. Sair")
        opcao = input("Opção: ")
        if opcao == "1": menu_quartos()
        elif opcao == "2": menu_clientes()
        elif opcao == "3": menu_reservas()
        elif opcao == "4": relatorio_ocupacao()
        elif opcao == "0":
            fazer_logout(utilizador)
            break
        else:
            print("Opção inválida.")

# Ponto de entrada
utilizador = fazer_login()
if utilizador:
    menu_principal(utilizador)