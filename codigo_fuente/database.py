"""
Modulo de acceso a datos (Data Access Layer).
Contiene todas las funciones que interactuan directamente con la base
de datos SQLite del sistema Registro de Clientes.
"""
import sqlite3
 
DB_NAME = "clientes.db"
 
 
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
 
 # Crea la tabla 'clientes' si aun no existe en la base de datos
def crear_tabla():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE,
            telefono TEXT,
            correo TEXT,
            direccion TEXT,
            fecha_registro TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()
 
 # Obtiene todos los clientes, o los filtra por nombre/DNI si se recibe un texto de busqueda
def obtener_clientes(filtro=""):
    conn = get_connection()
    if filtro:
        query = "SELECT * FROM clientes WHERE nombre LIKE ? OR dni LIKE ? ORDER BY id DESC"
        like = f"%{filtro}%"
        clientes = conn.execute(query, (like, like)).fetchall()
    else:
        clientes = conn.execute("SELECT * FROM clientes ORDER BY id DESC").fetchall()
    conn.close()
    return clientes
 
 # Busca un cliente especifico por su ID (usado en la pantalla de edicion)
def obtener_cliente_por_id(cliente_id):
    conn = get_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    conn.close()
    return cliente
 
 # Inserta un nuevo cliente en la base de datos
def insertar_cliente(nombre, dni, telefono, correo, direccion):
    conn = get_connection()
    conn.execute(
        "INSERT INTO clientes (nombre, dni, telefono, correo, direccion) VALUES (?, ?, ?, ?, ?)",
        (nombre, dni, telefono, correo, direccion),
    )
    conn.commit()
    conn.close()
 
 # Actualiza los datos de un cliente existente, identificado por su ID
def actualizar_cliente(cliente_id, nombre, dni, telefono, correo, direccion):
    conn = get_connection()
    conn.execute(
        """UPDATE clientes
           SET nombre = ?, dni = ?, telefono = ?, correo = ?, direccion = ?
           WHERE id = ?""",
        (nombre, dni, telefono, correo, direccion, cliente_id),
    )
    conn.commit()
    conn.close()
 
 # Elimina un cliente de la base de datos, identificado por su ID
def eliminar_cliente(cliente_id):
    conn = get_connection()
    conn.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()