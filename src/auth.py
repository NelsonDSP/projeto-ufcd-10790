import hashlib
from database import criar_ligacao, hash_password

def fazer_login():
    """Pede as credenciais ao utilizador e valida na base de dados."""
    print("\n===== LOGIN =====")
    username = input("Username: ")
    password = input("Password: ")

    conn = criar_ligacao()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        SELECT id, nome, perfil FROM utilizadores
        WHERE username = ? AND password = ?
    """, (username, password_hash))

    utilizador = cursor.fetchone()
    conn.close()

    if utilizador:
        print(f"\nBem-vindo, {utilizador[1]}! Perfil: {utilizador[2]}")
        return {"id": utilizador[0], "nome": utilizador[1], "perfil": utilizador[2]}
    else:
        print("\nUsername ou password incorretos.")
        return None

def fazer_logout(utilizador):
    """Termina a sessão do utilizador."""
    print(f"\nSessão terminada. Até logo, {utilizador['nome']}!")