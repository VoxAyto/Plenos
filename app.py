
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('iniciativas_pleno_final.db')
    conn.row_factory = sqlite3.Row

    grupos = ["VOX", "PP", "PSOE", "COMPROMIS", "PODEMOS", "CIUDADANOS"]
    resultados = ["APROBADO", "RECHAZADO", "RETIRADO"]
    fechas = [row["fecha"] for row in conn.execute("SELECT DISTINCT fecha FROM iniciativas ORDER BY fecha DESC").fetchall()]
    concejales_vox = ["", "MARIO", "PEPE", "CARMEN", "JUAN", "OSCAR"]

    grupo = request.args.get('grupo', '')
    palabra_clave = request.args.get('palabra_clave', '')
    resultado = request.args.get('resultado', '')
    fecha = request.args.get('fecha', '')
    concejal = request.args.get('concejal', '')
se_ha_buscado = any([grupo, palabra_clave, resultado, fecha, concejal])

    query = "SELECT fecha, grupo, contenido, resultado, concejal FROM iniciativas WHERE 1=1"
    params = []

    if grupo:
        query += " AND grupo = ?"
        params.append(grupo)
    if palabra_clave:
        query += " AND contenido LIKE ?"
        params.append(f"%{palabra_clave}%")
    if resultado:
        query += " AND resultado = ?"
        params.append(resultado)
    if fecha:
        query += " AND fecha = ?"
        params.append(fecha)
    if grupo == "VOX" and concejal:
        query += " AND concejal = ?"
        params.append(concejal)

    resultados_query = conn.execute(query, params).fetchall() if se_ha_buscado else []

    return render_template('index.html', resultados=resultados_query, grupos=grupos,
                           resultados_filtro=resultados, fechas=fechas, grupo=grupo,
                           palabra_clave=palabra_clave, resultado=resultado, fecha=fecha,
                           concejales=concejales_vox, concejal=concejal)

if __name__ == '__main__':
    app.run(debug=True)
