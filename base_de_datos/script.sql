-- Script de creacion de la base de datos
-- Proyecto: Registro de Clientes
-- Motor: SQLite
 
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    telefono TEXT,
    correo TEXT,
    direccion TEXT,
    fecha_registro TEXT DEFAULT (datetime('now','localtime'))
);
 
-- Notas de diseno:
-- id: clave primaria autoincremental
-- nombre: obligatorio
-- dni: obligatorio y unico (evita clientes duplicados)
-- telefono, correo, direccion: opcionales
-- fecha_registro: se llena automaticamente con la fecha y hora del registro