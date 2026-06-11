from auth import fazer_login, fazer_logout

utilizador = fazer_login()

if utilizador:
    fazer_logout(utilizador)