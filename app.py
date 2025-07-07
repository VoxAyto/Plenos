from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('iniciativas_pleno.db')
    return conn

@app.route('/')
def index():
    grupo = request.args.get('grupo', '').strip()
    titulo = request.args.get('titulo', '').strip()
    resultado = request.args.get('resultado', '').strip()
    fecha = request.args.get('fecha', '').strip()

    conn = get_db_connection()

    # Obtener valores únicos para desplegables
    grupos = [row[0] for row in conn.execute("SELECT DISTINCT grupo FROM iniciativas ORDER BY grupo")]
    resultados = [row[0] for row in conn.execute("SELECT DISTINCT resultado FROM iniciativas ORDER BY resultado")]
    fechas = [row[0] for row in conn.execute("SELECT DISTINCT fecha FROM iniciativas ORDER BY fecha DESC")]

    # Construir consulta dinámica
    query = "SELECT fecha, grupo, titulo, resultado, archivo FROM iniciativas WHERE 1=1"
    params = []

    if grupo:
        query += " AND grupo = ?"
        params.append(grupo)
    if titulo:
        query += " AND titulo LIKE ?"
        params.append(f"%{titulo}%")
    if resultado:
        query += " AND resultado = ?"
        params.append(resultado)
    if fecha:
        query += " AND fecha = ?"
        params.append(fecha)

    resultados_query = conn.execute(query, params).fetchall()
    conn.close()
return render_template('index.html',
                       resultados=resultados_query,
                       grupos=grupos,
                       opciones_resultado=resultados,
                       fechas=fechas)

if __name__ == '__main__':
    app.run(debug=True)
