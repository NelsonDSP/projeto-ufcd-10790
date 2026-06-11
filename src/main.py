from auth import fazer_login, fazer_logout
from quartos import adicionar_quarto, listar_quartos

utilizador = fazer_login()

if utilizador:
    adicionar_quarto()
    listar_quartos()
    fazer_logout(utilizador)