from flask import Blueprint, render_template, request, redirect, url_for
from .models import get_db

main = Blueprint('main', __name__)

# Pantalla de inicio
@main.route("/")
def index():
    return render_template("inicio.html")

# Vista de despachos del día
@main.route("/despachos")
def ver_despachos():
    db = get_db()
    cursor = db.execute("""
        SELECT d.id, p.id AS pedido_id, p.canal, p.fecha,
               d.sku, d.color, d.cantidad, d.estado
        FROM pedidos p
        JOIN detalle_pedidos d ON p.id = d.pedido_id
        ORDER BY p.fecha DESC
    """)
    despachos = cursor.fetchall()
    return render_template("base.html", despachos=despachos)

# Formulario para ingresar nuevo pedido
@main.route("/nuevo", methods=["GET", "POST"])
def nuevo_pedido():
    if request.method == "POST":
        canal = request.form["canal"]
        fecha = request.form["fecha"]
        db = get_db()
        cursor = db.cursor()

        # Insertar pedido principal
        cursor.execute("INSERT INTO pedidos (canal, fecha) VALUES (?, ?)", (canal, fecha))
        pedido_id = cursor.lastrowid

        # Insertar detalle del pedido (productos)
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

# Botón para cambiar el estado de un producto
@main.route("/actualizar_estado/<int:detalle_id>/<string:nuevo_estado>", methods=["POST"])
def actualizar_estado(detalle_id, nuevo_estado):
    db = get_db()
    db.execute("UPDATE detalle_pedidos SET estado = ? WHERE id = ?", (nuevo_estado, detalle_id))
    db.commit()
    return redirect(url_for("main.ver_despachos"))
