from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    conn = sqlite3.connect("iniciativas_pleno_limpia.db")
    conn.row_factory = sqlite3.Row

    grupo = request.args.get("grupo", "")
    titulo = request.args.get("titulo", "")
    resultado = request.args.get("resultado", "")
    fecha = request.args.get("fecha", "")

    query = "SELECT fecha, grupo, contenido, resultado FROM iniciativas WHERE 1=1"
    params = []

    if grupo:
        query += " AND grupo = ?"
        params.append(grupo)
    if titulo:
        query += " AND contenido LIKE ?"
        params.append(f"%{titulo}%")
    if resultado:
        query += " AND resultado = ?"
        params.append(resultado)
    if fecha:
        query += " AND fecha = ?"
        params.append(fecha)

    resultados = conn.execute(query, params).fetchall()

    grupos = [row[0] for row in conn.execute("SELECT DISTINCT grupo FROM iniciativas ORDER BY grupo")]
    resultados_list = [row[0] for row in conn.execute("SELECT DISTINCT resultado FROM iniciativas ORDER BY resultado")]
    fechas = [row[0] for row in conn.execute("SELECT DISTINCT fecha FROM iniciativas ORDER BY fecha DESC")]
    conn.close()

    return render_template("index.html", resultados=resultados,
                           grupos=grupos, resultados_list=resultados_list, fechas=fechas)
