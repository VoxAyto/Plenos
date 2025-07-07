from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('iniciativas_pleno_final.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()

    # Obtener opciones filtradas y limpias
    grupos = [row["grupo"] for row in conn.execute(
        "SELECT DISTINCT grupo FROM iniciativas WHERE grupo IN ('VOX', 'PP', 'PSOE', 'COMPROMIS', 'PODEMOS')").fetchall()]

    resultados = [row["resultado"] for row in conn.execute(
        "SELECT DISTINCT resultado FROM iniciativas WHERE resultado != ''").fetchall()]

    fechas = sorted(set(row["fecha"][:4] for row in conn.execute(
        "SELECT DISTINCT fecha FROM iniciativas WHERE fecha LIKE '20%'").fetchall()))

    # Filtrado de resultados
    grupo = request.args.get('grupo', '')
    titulo = request.args.get('titulo', '')
    resultado = request.args.get('resultado', '')
    fecha = request.args.get('fecha', '')

    query = "SELECT fecha, grupo, contenido, resultado FROM iniciativas WHERE 1=1"
    params = {}

    if grupo:
        query += " AND grupo = :grupo"
        params["grupo"] = grupo
    if titulo:
        query += " AND contenido LIKE :titulo"
        params["titulo"] = f"%{titulo}%"
    if resultado:
        query += " AND resultado = :resultado"
        params["resultado"] = resultado
    if fecha:
        query += " AND fecha LIKE :fecha"
        params["fecha"] = f"{fecha}%"

    resultados = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('index.html',
                           resultados=resultados,
                           grupos=grupos,
                           resultados_opciones=resultados,
                           fechas=fechas)