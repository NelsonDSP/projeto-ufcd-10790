import sqlite3
import hashlib

# criação da base de dados e das tabelas necessárias para o sistema de gestão hoteleira
def criar_ligacao():
    return sqlite3.connect("hotel.db")

# para a password ficar em hash e não em texto simples na base de dados, aumentando a segurança do sistema
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# criação das tabelas: utilizadores, clientes, quartos e reservas, com as respetivas colunas e tipos de dados
def criar_tabelas():
    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contacto TEXT,
            documento TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quartos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            preco_noite REAL NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            quarto_id INTEGER NOT NULL,
            checkin TEXT NOT NULL,
            checkout TEXT NOT NULL,
            estado TEXT NOT NULL,
            valor_total REAL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (quarto_id) REFERENCES quartos(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Base de dados criada com sucesso!")

def criar_admin_inicial():
    """Cria um utilizador admin por defeito se não existir nenhum."""
    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM utilizadores")
    total = cursor.fetchone()[0]

    if total == 0:
        password_hash = hash_password("admin123")
        cursor.execute("""
            INSERT INTO utilizadores (nome, username, password, perfil)
            VALUES (?, ?, ?, ?)
        """, ("Administrador", "admin", password_hash, "admin"))
        conn.commit()
        print("Utilizador admin criado! Username: admin | Password: admin123")

    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    criar_admin_inicial()