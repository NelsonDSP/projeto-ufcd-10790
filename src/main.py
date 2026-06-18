from auth import fazer_login, fazer_logout
from reservas import fazer_reserva, listar_reservas

utilizador = fazer_login()

if utilizador:
    fazer_reserva()
    listar_reservas()
    fazer_logout(utilizador)
    
#admin admin123
