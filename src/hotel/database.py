import sqlite3
import bcrypt

# Função para criar uma ligação à base de dados SQLite
def criar_ligacao():
    return sqlite3.connect("hotel.db")

def criar_tabelas():
    """Cria todas as tabelas da base de dados se não existirem."""
    conn = criar_ligacao()
    cursor = conn.cursor()

    # Tabela de utilizadores (rececionistas, gestores, admins)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            perfil TEXT NOT NULL  -- 'rececionista', 'gestor', 'admin'
        )
    """)

    # Tabela de clientes (hóspedes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contacto TEXT,
            documento TEXT
        )
    """)

    # Tabela de quartos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quartos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,      -- 'single', 'double', 'suite'
            preco_noite REAL NOT NULL,
            estado TEXT NOT NULL     -- 'disponivel', 'ocupado'
        )
    """)

    # Tabela de reservas (liga clientes a quartos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            quarto_id INTEGER NOT NULL,
            checkin TEXT NOT NULL,   -- formato 'YYYY-MM-DD'
            checkout TEXT NOT NULL,
            estado TEXT NOT NULL,    -- 'confirmada', 'cancelada', 'checkin', 'checkout'
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
        password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        cursor.execute("""
            INSERT INTO utilizadores (nome, username, password, perfil)
            VALUES (?, ?, ?, ?)
        """, ("Administrador", "admin", password_hash, "admin"))
        conn.commit()
        print("Utilizador admin criado! Username: admin | Password: admin123")

    conn.close()

# Quando este ficheiro é executado diretamente
if __name__ == "__main__":
    criar_tabelas()
    criar_admin_inicial()