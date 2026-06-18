from database import criar_ligacao
from datetime import datetime

def fazer_checkin():
    print("\n===== CHECK-IN =====")

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

    if reserva[5] != "confirmada":
        print(f"Esta reserva não pode fazer check-in. Estado actual: {reserva[5]}")
        conn.close()
        return

    print(f"\nCliente : {reserva[1]}")
    print(f"Quarto  : {reserva[2]}")
    print(f"Período : {reserva[3]} a {reserva[4]}")

    confirmacao = input("\nConfirmar check-in? (s/n): ")
    if confirmacao.lower() != "s":
        print("Operação cancelada.")
        conn.close()
        return

    # Actualizar estado da reserva e do quarto
    cursor.execute("UPDATE reservas SET estado = 'checkin' WHERE id = ?", (reserva_id,))
    cursor.execute("""
        UPDATE quartos SET estado = 'ocupado'
        WHERE id = (SELECT quarto_id FROM reservas WHERE id = ?)
    """, (reserva_id,))

    conn.commit()
    conn.close()
    print(f"Check-in efectuado com sucesso! Bem-vindo, {reserva[1]}!")

def fazer_checkout():
    """Regista a saída do cliente e liberta o quarto."""
    print("\n===== CHECK-OUT =====")

    try:
        reserva_id = int(input("ID da reserva: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_ligacao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, c.nome, q.numero, q.tipo, r.checkin, r.checkout, r.estado, r.valor_total
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

    if reserva[6] != "checkin":
        print(f"Esta reserva não pode fazer check-out. Estado actual: {reserva[6]}")
        conn.close()
        return

    print(f"\nCliente : {reserva[1]}")
    print(f"Quarto  : {reserva[2]} ({reserva[3]})")
    print(f"Período : {reserva[4]} a {reserva[5]}")
    print(f"Total a pagar: €{reserva[7]:.2f}")

    confirmacao = input("\nConfirmar check-out? (s/n): ")
    if confirmacao.lower() != "s":
        print("Operação cancelada.")
        conn.close()
        return

    # Actualizar estado da reserva e libertar o quarto
    cursor.execute("UPDATE reservas SET estado = 'checkout' WHERE id = ?", (reserva_id,))
    cursor.execute("""
        UPDATE quartos SET estado = 'disponivel'
        WHERE id = (SELECT quarto_id FROM reservas WHERE id = ?)
    """, (reserva_id,))

    conn.commit()
    conn.close()
    print(f"Check-out efectuado! Obrigado, {reserva[1]}. Até à próxima!")