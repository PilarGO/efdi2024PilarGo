from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Ruta para recibir datos y escribir en la base de datos SQLite
@app.route('/update', methods=['POST'])
def update():
    data = request.form
    id_rec = data.get('id')
    ubicacion = data.get('ubicacion')
    medida = data.get('medida')
    cliente_ip = request.remote_addr

    # Validación de datos
    if not id_rec or not ubicacion or not medida:
        return jsonify({"status": "error", "message": "Datos incompletos"}), 400

    print("Datos recibidos del ESP32:")
    print("ID:", id_rec)
    print("Ubicación:", ubicacion)
    print("Medida:", medida)
    print("IP del Cliente:", cliente_ip)

    conn = None
    try:
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect('recipientes.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historico (
                            id TEXT,
                            ubicacion TEXT,
                            medida REAL,
                            ip TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')

        # Insertar los datos
        cursor.execute("INSERT INTO historico (id, ubicacion, medida, ip) VALUES (?, ?, ?, ?)",
                       (id_rec, ubicacion, float(medida), cliente_ip))
        conn.commit()
        return jsonify({"status": "success", "message": "Datos guardados correctamente"}), 200
    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": f"Error en SQLite: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
