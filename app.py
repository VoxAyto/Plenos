
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('iniciativas_pleno.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    
    # Obtener opciones únicas para los desplegables
grupos = [row["grupo"] for row in conn.execute(
    "SELECT DISTINCT grupo FROM iniciativas WHERE grupo IN ('VOX', 'PP', 'PSOE', 'COMPROMIS', 'PODEMOS')").fetchall()]
resultados = [row["resultado"] for row in conn.execute(
    "SELECT DISTINCT resultado FROM iniciativas WHERE resultado != ''").fetchall()]
fechas = sorted(set(row["fecha"][:4] for row in conn.execute(
    "SELECT DISTINCT fecha FROM iniciativas WHERE fecha LIKE '20%'").fetchall()))
    # Parámetros de búsqueda
    grupo = request.args.get("grupo", "")
    titulo = request.args.get("titulo", "")
    resultado = request.args.get("resultado", "")
    fecha = request.args.get("fecha", "")

    query = "SELECT fecha, grupo, contenido, resultado FROM iniciativas WHERE 1=1"
    params = []

    if grupo:
        query += " AND grupo LIKE ?"
        params.append(f"%{grupo}%")
    if titulo:
        query += " AND contenido LIKE ?"
        params.append(f"%{titulo}%")
    if resultado:
        query += " AND resultado LIKE ?"
        params.append(f"%{resultado}%")
    if fecha:
        query += " AND fecha = ?"
        params.append(fecha)

    resultados = conn.execute(query, params).fetchall()
    conn.close()

    return render_template("index.html",
                           resultados=resultados,
                           grupos=grupos,
                           fechas=fechas,
                           resultados_opciones=resultados_opciones)
