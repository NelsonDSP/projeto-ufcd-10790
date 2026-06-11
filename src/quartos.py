from database import criar_ligacao

# adição, edição, remoção e consulta de quartos do hotel
def adicionar_quarto():
    print("\n===== ADICIONAR QUARTO =====")
    numero = input("Número do quarto: ")
    print("Tipos disponíveis: single, double, suite")
    tipo = input("Tipo: ").lower()
    preco = input("Preço por noite (€): ")

    try:
        preco = float(preco)
    except ValueError:
        print("Preço inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    # Verificar se o número do quarto já existe
    cursor.execute("SELECT id FROM quartos WHERE numero = ?", (numero,))
    if cursor.fetchone():
        print(f"Já existe um quarto com o número {numero}.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO quartos (numero, tipo, preco_noite, estado)
        VALUES (?, ?, ?, 'disponivel')
    """, (numero, tipo, preco))

    conn.commit()
    conn.close()
    print(f"Quarto {numero} adicionado com sucesso!")

def listar_quartos():
    print("\n===== LISTA DE QUARTOS =====")
    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("SELECT id, numero, tipo, preco_noite, estado FROM quartos")
    quartos = cursor.fetchall()
    conn.close()

    if not quartos:
        print("Não existem quartos registados.")
        return

    print(f"{'ID':<5} {'Número':<10} {'Tipo':<10} {'Preço/Noite':<15} {'Estado'}")
    print("-" * 55)
    for q in quartos:
        print(f"{q[0]:<5} {q[1]:<10} {q[2]:<10} €{q[3]:<14.2f} {q[4]}")

def editar_quarto():
    listar_quartos()
    print("\n===== EDITAR QUARTO =====")
    try:
        quarto_id = int(input("ID do quarto a editar: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quartos WHERE id = ?", (quarto_id,))
    quarto = cursor.fetchone()

    if not quarto:
        print("Quarto não encontrado.")
        conn.close()
        return

    print(f"\nQuarto actual: Número {quarto[1]} | {quarto[2]} | €{quarto[3]}/noite | {quarto[4]}")
    print("(Deixa em branco para manter o valor actual)")

    numero = input(f"Novo número [{quarto[1]}]: ") or quarto[1]
    tipo = input(f"Novo tipo [{quarto[2]}]: ") or quarto[2]
    preco = input(f"Novo preço [{quarto[3]}]: ") or quarto[3]
    estado = input(f"Novo estado [{quarto[4]}]: ") or quarto[4]

    try:
        preco = float(preco)
    except ValueError:
        print("Preço inválido.")
        conn.close()
        return

    cursor.execute("""
        UPDATE quartos SET numero = ?, tipo = ?, preco_noite = ?, estado = ?
        WHERE id = ?
    """, (numero, tipo, preco, estado, quarto_id))

    conn.commit()
    conn.close()
    print("Quarto actualizado com sucesso!")

def remover_quarto():
    listar_quartos()
    print("\n===== REMOVER QUARTO =====")
    try:
        quarto_id = int(input("ID do quarto a remover: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("SELECT numero FROM quartos WHERE id = ?", (quarto_id,))
    quarto = cursor.fetchone()

    if not quarto:
        print("Quarto não encontrado.")
        conn.close()
        return

    confirmacao = input(f"Tens a certeza que queres remover o quarto {quarto[0]}? (s/n): ")
    if confirmacao.lower() != "s":
        print("Operação cancelada.")
        conn.close()
        return

    cursor.execute("DELETE FROM quartos WHERE id = ?", (quarto_id,))
    conn.commit()
    conn.close()
    print(f"Quarto {quarto[0]} removido com sucesso!")

def consultar_disponibilidade():
    print("\n===== CONSULTAR DISPONIBILIDADE =====")
    checkin = input("Data de check-in (YYYY-MM-DD): ")
    checkout = input("Data de check-out (YYYY-MM-DD): ")

    conn = criar_ligacao()
    cursor = conn.cursor()

    # Quartos que NÃO têm reserva confirmada ou em checkin nesse período
    cursor.execute("""
        SELECT id, numero, tipo, preco_noite FROM quartos
        WHERE estado = 'disponivel'
        AND id NOT IN (
            SELECT quarto_id FROM reservas
            WHERE estado IN ('confirmada', 'checkin')
            AND NOT (checkout <= ? OR checkin >= ?)
        )
    """, (checkin, checkout))

    quartos = cursor.fetchall()
    conn.close()

    if not quartos:
        print("Não há quartos disponíveis para esse período.")
        return

    print(f"\n{'ID':<5} {'Número':<10} {'Tipo':<10} {'Preço/Noite'}")
    print("-" * 40)
    for q in quartos:
        print(f"{q[0]:<5} {q[1]:<10} {q[2]:<10} €{q[3]:.2f}")