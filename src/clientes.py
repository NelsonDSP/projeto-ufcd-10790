from database import criar_ligacao

def registar_cliente():
    print("\n===== REGISTAR CLIENTE =====")
    nome = input("Nome completo: ")
    email = input("Email: ")
    contacto = input("Contacto (telemóvel): ")
    documento = input("Documento de identidade (BI/CC/Passaporte): ")

    conn = criar_ligacao()
    cursor = conn.cursor()

    # Verifica se o email já existe
    cursor.execute("SELECT id FROM clientes WHERE email = ?", (email,))
    if cursor.fetchone():
        print("Já existe um cliente com esse email.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO clientes (nome, email, contacto, documento)
        VALUES (?, ?, ?, ?)
    """, (nome, email, contacto, documento))

    conn.commit()
    conn.close()
    print(f"Cliente {nome} registado com sucesso!")

def listar_clientes():
    print("\n===== LISTA DE CLIENTES =====")
    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email, contacto, documento FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    if not clientes:
        print("Não existem clientes registados.")
        return

    print(f"{'ID':<5} {'Nome':<25} {'Email':<30} {'Contacto':<15} {'Documento'}")
    print("-" * 85)
    for c in clientes:
        print(f"{c[0]:<5} {c[1]:<25} {c[2]:<30} {c[3]:<15} {c[4]}")

def procurar_cliente():
    print("\n===== PROCURAR CLIENTE =====")
    termo = input("Nome ou email: ")

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, contacto, documento FROM clientes
        WHERE nome LIKE ? OR email LIKE ?
    """, (f"%{termo}%", f"%{termo}%"))

    clientes = cursor.fetchall()
    conn.close()

    if not clientes:
        print("Nenhum cliente encontrado.")
        return clientes

    print(f"\n{'ID':<5} {'Nome':<25} {'Email':<30} {'Contacto':<15} {'Documento'}")
    print("-" * 85)
    for c in clientes:
        print(f"{c[0]:<5} {c[1]:<25} {c[2]:<30} {c[3]:<15} {c[4]}")

    return clientes

def historico_cliente():
    print("\n===== HISTÓRICO DE RESERVAS =====")
    try:
        cliente_id = int(input("ID do cliente: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    if not cliente:
        print("Cliente não encontrado.")
        conn.close()
        return

    cursor.execute("""
        SELECT r.id, q.numero, q.tipo, r.checkin, r.checkout, r.estado, r.valor_total
        FROM reservas r
        JOIN quartos q ON r.quarto_id = q.id
        WHERE r.cliente_id = ?
        ORDER BY r.checkin DESC
    """, (cliente_id,))

    reservas = cursor.fetchall()
    conn.close()

    print(f"\nHistórico de {cliente[0]}:")
    if not reservas:
        print("Sem reservas registadas.")
        return

    print(f"{'ID':<5} {'Quarto':<10} {'Tipo':<10} {'Check-in':<12} {'Check-out':<12} {'Estado':<12} {'Total'}")
    print("-" * 75)
    for r in reservas:
        total = f"€{r[6]:.2f}" if r[6] else "—"
        print(f"{r[0]:<5} {r[1]:<10} {r[2]:<10} {r[3]:<12} {r[4]:<12} {r[5]:<12} {total}")