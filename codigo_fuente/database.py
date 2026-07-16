import sqlite3
 
DB_NAME = "clientes.db"
 
 
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
 
 
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
 
 
def obtener_cliente_por_id(cliente_id):
    conn = get_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    conn.close()
    return cliente
 
 
def insertar_cliente(nombre, dni, telefono, correo, direccion):
    conn = get_connection()
    conn.execute(
        "INSERT INTO clientes (nombre, dni, telefono, correo, direccion) VALUES (?, ?, ?, ?, ?)",
        (nombre, dni, telefono, correo, direccion),
    )
    conn.commit()
    conn.close()
 
 
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
 
 
def eliminar_cliente(cliente_id):
    conn = get_connection()
    conn.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()