"""
Controlador principal de la aplicacion Flask.
Define las rutas (endpoints) del sistema Registro de Clientes y conecta
las peticiones del usuario con el modulo database.py.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import database as db

app = Flask(__name__)
app.secret_key = "clave-secreta-registro-clientes"

# Ruta principal: muestra el listado de clientes y permite buscar por nombre o DNI
@app.route("/")
def index():
    filtro = request.args.get("q", "")
    clientes = db.obtener_clientes(filtro)
    return render_template("index.html", clientes=clientes, filtro=filtro)

# Ruta para registrar un nuevo cliente (GET muestra el formulario, POST guarda los datos)
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        dni = request.form["dni"].strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        direccion = request.form.get("direccion", "").strip()

        if not nombre or not dni:
            flash("Nombre y DNI son obligatorios.", "danger")
            return redirect(url_for("registrar"))
        
        if not dni.isdigit() or len(dni) != 8:
            flash("El DNI debe tener exactamente 8 numeros.", "danger")
            return redirect(url_for("registrar")) 

        try:
            db.insertar_cliente(nombre, dni, telefono, correo, direccion)
            flash("Cliente registrado correctamente.", "success")
            return redirect(url_for("index"))
        except Exception:
            flash("Ya existe un cliente con ese DNI.", "danger")
            return redirect(url_for("registrar"))

    return render_template("form.html", cliente=None, accion="Registrar")

# Ruta para editar un cliente existente (GET carga sus datos, POST guarda los cambios)
@app.route("/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = db.obtener_cliente_por_id(cliente_id)
    if cliente is None:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        dni = request.form["dni"].strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        direccion = request.form.get("direccion", "").strip()
        if not dni.isdigit() or len(dni) != 8:
            flash("El DNI debe tener exactamente 8 numeros.", "danger")
            return redirect(url_for("editar", cliente_id=cliente_id))

        db.actualizar_cliente(cliente_id, nombre, dni, telefono, correo, direccion)
        flash("Cliente actualizado correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", cliente=cliente, accion="Editar")

# Ruta para eliminar un cliente del sistema
@app.route("/eliminar/<int:cliente_id>")
def eliminar(cliente_id):
    db.eliminar_cliente(cliente_id)
    flash("Cliente eliminado correctamente.", "success")
    return redirect(url_for("index"))

# Punto de entrada: crea la tabla si no existe y ejecuta el servidor Flask
if __name__ == "__main__":
    db.crear_tabla()
    app.run(debug=True)