from database import criar_ligacao
from datetime import datetime

def calcular_noites(checkin, checkout):
    """Calcula o número de noites entre duas datas."""
    fmt = "%Y-%m-%d"
    d1 = datetime.strptime(checkin, fmt)
    d2 = datetime.strptime(checkout, fmt)
    return (d2 - d1).days

def fazer_reserva():
    """Cria uma nova reserva para um cliente."""
    print("\n===== EFECTUAR RESERVA =====")

    try:
        cliente_id = int(input("ID do cliente: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    # Verificar se o cliente existe
    cursor.execute("SELECT nome FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    if not cliente:
        print("Cliente não encontrado.")
        conn.close()
        return

    checkin = input("Data de check-in (YYYY-MM-DD): ")
    checkout = input("Data de check-out (YYYY-MM-DD): ")

    # Validar datas
    try:
        noites = calcular_noites(checkin, checkout)
        if noites <= 0:
            print("A data de checkout deve ser posterior ao check-in.")
            conn.close()
            return
    except ValueError:
        print("Formato de data inválido. Usa YYYY-MM-DD.")
        conn.close()
        return

    # Mostrar quartos disponíveis para o período
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

    if not quartos:
        print("Não há quartos disponíveis para esse período.")
        conn.close()
        return

    print(f"\nQuartos disponíveis para {checkin} a {checkout}:")
    print(f"{'ID':<5} {'Número':<10} {'Tipo':<10} {'Preço/Noite'}")
    print("-" * 40)
    for q in quartos:
        print(f"{q[0]:<5} {q[1]:<10} {q[2]:<10} €{q[3]:.2f}")

    try:
        quarto_id = int(input("\nID do quarto: "))
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    # Verificar se o quarto escolhido está na lista de disponíveis
    quarto_escolhido = next((q for q in quartos if q[0] == quarto_id), None)
    if not quarto_escolhido:
        print("Quarto inválido ou não disponível.")
        conn.close()
        return

    valor_total = quarto_escolhido[3] * noites

    print(f"\nResumo da reserva:")
    print(f"  Cliente : {cliente[0]}")
    print(f"  Quarto  : {quarto_escolhido[1]} ({quarto_escolhido[2]})")
    print(f"  Período : {checkin} a {checkout} ({noites} noite(s))")
    print(f"  Total   : €{valor_total:.2f}")

    confirmacao = input("\nConfirmar reserva? (s/n): ")
    if confirmacao.lower() != "s":
        print("Reserva cancelada.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO reservas (cliente_id, quarto_id, checkin, checkout, estado, valor_total)
        VALUES (?, ?, ?, ?, 'confirmada', ?)
    """, (cliente_id, quarto_id, checkin, checkout, valor_total))

    conn.commit()
    conn.close()
    print("Reserva efectuada com sucesso!")

def cancelar_reserva():
    """Cancela uma reserva existente."""
    print("\n===== CANCELAR RESERVA =====")

    try:
        reserva_id = int(input("ID da reserva: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, c.nome, q.numero, r.checkin, r.checkout, r.estado
        FROM reservas r
        JOIN clientes c ON r.cliente_id = c.id
        JOIN quartos q ON r.quarto_id = q.id
        WHERE r.id = ?
    """, (reserva_id,))

    reserva = cursor.fetchone()

    if not reserva:
        print("Reserva não encontrada.")
        conn.close()
        return

    if reserva[5] in ("cancelada", "checkout"):
        print(f"Esta reserva já está no estado '{reserva[5]}', não pode ser cancelada.")
        conn.close()
        return

    print(f"\nReserva: Cliente {reserva[1]} | Quarto {reserva[2]} | {reserva[3]} a {reserva[4]}")
    confirmacao = input("Confirmar cancelamento? (s/n): ")

    if confirmacao.lower() != "s":
        print("Operação cancelada.")
        conn.close()
        return

    cursor.execute("UPDATE reservas SET estado = 'cancelada' WHERE id = ?", (reserva_id,))
    conn.commit()
    conn.close()
    print("Reserva cancelada com sucesso!")

def listar_reservas():
    """Lista todas as reservas do sistema."""
    print("\n===== LISTA DE RESERVAS =====")

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, c.nome, q.numero, q.tipo, r.checkin, r.checkout, r.estado, r.valor_total
        FROM reservas r
        JOIN clientes c ON r.cliente_id = c.id
        JOIN quartos q ON r.quarto_id = q.id
        ORDER BY r.checkin DESC
    """)

    reservas = cursor.fetchall()
    conn.close()

    if not reservas:
        print("Não existem reservas registadas.")
        return

    print(f"{'ID':<5} {'Cliente':<20} {'Quarto':<8} {'Tipo':<10} {'Check-in':<12} {'Check-out':<12} {'Estado':<12} {'Total'}")
    print("-" * 90)
    for r in reservas:
        total = f"€{r[7]:.2f}" if r[7] else "—"
        print(f"{r[0]:<5} {r[1]:<20} {r[2]:<8} {r[3]:<10} {r[4]:<12} {r[5]:<12} {r[6]:<12} {total}")