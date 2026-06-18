from auth import fazer_login, fazer_logout
from checkinout import fazer_checkin, fazer_checkout
from reservas import listar_reservas

utilizador = fazer_login()

if utilizador:
    listar_reservas()
    fazer_checkin()
    listar_reservas()
    fazer_checkout()
    listar_reservas()
    fazer_logout(utilizador)
    
#admin admin123    ID:1
