from database import criar_ligacao
from datetime import datetime

def relatorio_ocupacao():
    print("\n===== RELATÓRIO DE OCUPAÇÃO =====")

    checkin = input("Data de início (YYYY-MM-DD): ")
    checkout = input("Data de fim (YYYY-MM-DD): ")

    conn = criar_ligacao()
    cursor = conn.cursor()

    # Total de quartos
    cursor.execute("SELECT COUNT(*) FROM quartos")
    total_quartos = cursor.fetchone()[0]

    # Reservas no período (confirmadas, checkin ou checkout)
    cursor.execute("""
        SELECT COUNT(DISTINCT quarto_id) FROM reservas
        WHERE estado IN ('confirmada', 'checkin', 'checkout')
        AND NOT (checkout <= ? OR checkin >= ?)
    """, (checkin, checkout))
    quartos_ocupados = cursor.fetchone()[0]

    # Receita total no período
    cursor.execute("""
        SELECT SUM(valor_total) FROM reservas
        WHERE estado IN ('confirmada', 'checkin', 'checkout')
        AND NOT (checkout <= ? OR checkin >= ?)
    """, (checkin, checkout))
    receita = cursor.fetchone()[0] or 0

    # Lista de reservas no período
    cursor.execute("""
        SELECT r.id, c.nome, q.numero, q.tipo, r.checkin, r.checkout, r.estado, r.valor_total
        FROM reservas r
        JOIN clientes c ON r.cliente_id = c.id
        JOIN quartos q ON r.quarto_id = q.id
        WHERE r.estado IN ('confirmada', 'checkin', 'checkout')
        AND NOT (r.checkout <= ? OR r.checkin >= ?)
        ORDER BY r.checkin
    """, (checkin, checkout))
    reservas = cursor.fetchall()
    conn.close()

    # Calcular taxa de ocupação
    if total_quartos > 0:
        taxa = (quartos_ocupados / total_quartos) * 100
    else:
        taxa = 0

    print(f"\nPeríodo       : {checkin} a {checkout}")
    print(f"Total quartos : {total_quartos}")
    print(f"Quartos ocupados: {quartos_ocupados}")
    print(f"Taxa de ocupação: {taxa:.1f}%")
    print(f"Receita total : €{receita:.2f}")

    if reservas:
        print(f"\n{'ID':<5} {'Cliente':<20} {'Quarto':<8} {'Tipo':<10} {'Check-in':<12} {'Check-out':<12} {'Estado':<12} {'Total'}")
        print("-" * 90)
        for r in reservas:
            total = f"€{r[7]:.2f}" if r[7] else "—"
            print(f"{r[0]:<5} {r[1]:<20} {r[2]:<8} {r[3]:<10} {r[4]:<12} {r[5]:<12} {r[6]:<12} {total}")