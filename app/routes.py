from flask import Blueprint, render_template, request, redirect, url_for
from .models import get_db

main = Blueprint('main', __name__)

# Inicio
@main.route("/")
def index():
    return render_template("inicio.html")

# Despachos agrupados por canal y pedido
@main.route("/despachos")
def ver_despachos():
    db = get_db()

    canal = request.args.get("canal", "")
    estado = request.args.get("estado", "")
    fecha = request.args.get("fecha", "")

    query = """
        SELECT d.id, p.id AS pedido_id, p.canal, p.fecha,
               d.sku, d.color, d.cantidad, d.estado
        FROM pedidos p
        JOIN detalle_pedidos d ON p.id = d.pedido_id
        WHERE 1=1
    """
    params = []

    if canal:
        query += " AND p.canal = ?"
        params.append(canal)

    if estado:
        query += " AND d.estado = ?"
        params.append(estado)

    if fecha:
        query += " AND p.fecha = ?"
        params.append(fecha)

    query += " ORDER BY p.canal, p.fecha DESC"

    cursor = db.execute(query, params)
    resultados = cursor.fetchall()

    # Agrupar por canal y luego por pedido_id
    despachos = {}
    for row in resultados:
        canal = row["canal"]
        pedido_id = row["pedido_id"]
        if canal not in despachos:
            despachos[canal] = {}
        if pedido_id not in despachos[canal]:
            despachos[canal][pedido_id] = []
        despachos[canal][pedido_id].append(row)

    return render_template("base.html", despachos=despachos)

# Nuevo pedido
@main.route("/nuevo", methods=["GET", "POST"])
def nuevo_pedido():
    if request.method == "POST":
        canal = request.form["canal"]
        fecha = request.form["fecha"]
        db = get_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO pedidos (canal, fecha) VALUES (?, ?)", (canal, fecha))
        pedido_id = cursor.lastrowid

        skus = request.form.getlist("sku")
        colores = request.form.getlist("color")
        cantidades = request.form.getlist("cantidad")

        for sku, color, cantidad in zip(skus, colores, cantidades):
            cursor.execute("""
                INSERT INTO detalle_pedidos (pedido_id, canal, sku, color, cantidad)
                VALUES (?, ?, ?, ?, ?)
            """, (pedido_id, canal, sku, color, cantidad))

        db.commit()
        return redirect(url_for("main.ver_despachos"))

    return render_template("nuevo.html")

# Cambiar estado
@main.route("/actualizar_estado/<int:detalle_id>/<string:nuevo_estado>", methods=["POST"])
def actualizar_estado(detalle_id, nuevo_estado):
    db = get_db()
    db.execute("UPDATE detalle_pedidos SET estado = ? WHERE id = ?", (nuevo_estado, detalle_id))
    db.commit()
    return redirect(url_for("main.ver_despachos"))

# Eliminar pedido completo
@main.route("/eliminar_pedido/<int:pedido_id>", methods=["POST"])
def eliminar_pedido(pedido_id):
    db = get_db()
    db.execute("DELETE FROM detalle_pedidos WHERE pedido_id = ?", (pedido_id,))
    db.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
    db.commit()
    return redirect(url_for("main.ver_despachos"))
