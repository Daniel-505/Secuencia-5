import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

# Ruta donde se almacena la base de datos
DATABASE = 'basededatos.db'

# Función para conectar a la base de datos
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return db

# Inicializar la base de datos y crear la tabla si no existe
def init_db():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valores (
                id_medicion INTEGER PRIMARY KEY AUTOINCREMENT,
                valor_sensor TEXT NOT NULL,
                time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )''')
        db.commit()
    print("Base de datos inicializada.")

@app.route('/')
def home():
    return "Bienvenido a la API de mediciones"

@app.route('/mediciones', methods=['POST'])
def mediciones():
    valorStr = request.form.get('medicion')
    if valorStr is None:
        return "Falta el parámetro 'medicion'", 400

    try:
        valor = int(valorStr)
    except ValueError:
        return "El valor de 'medicion' no es válido", 400

    try:
        db = get_db()
        db.execute("INSERT INTO valores (valor_sensor) VALUES (?)", (valor,))
        db.commit()
    except sqlite3.Error as e:
        return f"Error de base de datos: {e}", 500

    return 'ok'

@app.route('/mediciones', methods=['GET'])
def get_mediciones():
    try:
        db = get_db()
        cursor = db.execute("SELECT id_medicion, valor_sensor, time_stamp FROM valores")
        filas = cursor.fetchall()

        # Renderizamos el HTML y pasamos los datos de la base de datos
        return render_template("mediciones.html", mediciones=filas)

    except sqlite3.Error as e:
        return f"Error de base de datos: {e}", 500

if __name__ == '__main__':
    init_db()  # Asegúrate de que la base de datos y la tabla se inicialicen
    app.run(host='0.0.0.0', port=5000)
