
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_PATH = 'iniciativas_pleno.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    grupo = request.args.get('grupo', '')
    resultado = request.args.get('resultado', '')
    titulo = request.args.get('titulo', '')
    fecha = request.args.get('fecha', '')

    query = "SELECT * FROM iniciativas WHERE 1=1"
    params = []

    if grupo:
        query += " AND grupo LIKE ?"
        params.append(f"%{grupo}%")
    if resultado:
        query += " AND resultado LIKE ?"
        params.append(f"%{resultado}%")
    if titulo:
        query += " AND contenido LIKE ?"
        params.append(f"%{titulo}%")
    if fecha:
        query += " AND fecha LIKE ?"
        params.append(f"%{fecha}%")

    conn = get_db_connection()
    iniciativas = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('index.html', iniciativas=iniciativas)

if __name__ == '__main__':
    app.run(debug=True)
