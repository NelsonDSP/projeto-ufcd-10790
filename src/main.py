from auth import fazer_login, fazer_logout
from quartos import listar_quartos
from clientes import registar_cliente, listar_clientes

utilizador = fazer_login()

if utilizador:
    registar_cliente()
    listar_clientes()
    fazer_logout(utilizador)