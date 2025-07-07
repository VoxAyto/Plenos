from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    conn = sqlite3.connect("iniciativas_pleno_final.db")
    conn.row_factory = sqlite3.Row

    grupos = ['VOX', 'PP', 'PSOE', 'COMPROMIS', 'PODEMOS']
    resultados = ['Aprobada', 'Rechazada', 'Retirada']
    fechas = [str(a) for a in range(2019, 2026)]

    query = "SELECT * FROM iniciativas WHERE 1=1"
    params = []

    grupo = request.args.get("grupo")
    if grupo:
        query += " AND grupo = ?"
        params.append(grupo)

    titulo = request.args.get("titulo")
    if titulo:
        query += " AND contenido LIKE ?"
        params.append(f"%{titulo}%")

    resultado = request.args.get("resultado")
    if resultado:
        query += " AND resultado = ?"
        params.append(resultado)

    fecha = request.args.get("fecha")
    if fecha:
        query += " AND fecha LIKE ?"
        params.append(f"{fecha}-%")

    resultados_query = conn.execute(query, params).fetchall()
    conn.close()

    return render_template("index.html",
                           resultados=resultados_query,
                           grupos=grupos,
                           resultados_filtro=resultados,
                           fechas=fechas)