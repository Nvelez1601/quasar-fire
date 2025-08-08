import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos de los satélites conocidos
SATELLITES = {
    "kenobi": {"position": [-500, -200]},
    "skywalker": {"position": [100, -100]},
    "sato": {"position": [500, 100]}
}

# Almacenamiento para el endpoint /topsecret_split/
satellite_data = {}

def get_location(distances):
    """
    Calcula la posición (x, y) del emisor del mensaje mediante trilateración.
    
    Args:
        distances: Lista de distancias a los satélites [kenobi, skywalker, sato]
    
    Returns:
        Tupla (x, y) con las coordenadas del emisor
    """
    # Posiciones de los satélites
    positions = [
        SATELLITES["kenobi"]["position"],
        SATELLITES["skywalker"]["position"],
        SATELLITES["sato"]["position"]
    ]
    
    # Construcción del sistema de ecuaciones
    A = []
    b = []
    for i in range(1, len(positions)):
        x1, y1 = positions[i-1]
        x2, y2 = positions[i]
        d1 = distances[i-1]
        d2 = distances[i]
        
        A.append([2*(x2 - x1), 2*(y2 - y1)])
        b.append(x2**2 - x1**2 + y2**2 - y1**2 + d1**2 - d2**2)
    
    # Resolución del sistema
    A = np.array(A)
    b = np.array(b)
    x, y = np.linalg.lstsq(A, b, rcond=None)[0]
    
    return float(x), float(y)

def get_message(messages):
    """
    Reconstruye el mensaje original a partir de las versiones parciales de los satélites.
    
    Args:
        messages: Lista de listas con los mensajes recibidos por cada satélite
    
    Returns:
        String con el mensaje reconstruido
    """
    max_len = max(len(msg) for msg in messages)
    full_message = []
    
    for i in range(max_len):
        word = ""
        for msg in messages:
            if i < len(msg) and msg[i] != "":
                word = msg[i]
                break  # Tomamos la primera palabra no vacía que encontremos
        full_message.append(word)
    
    return " ".join(full_message).strip()

# Endpoint para el Nivel 2
@app.route('/topsecret/', methods=['POST'])
def topsecret():
    data = request.get_json()
    
    if not data or 'satellites' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    satellites = data['satellites']
    
    # Validación básica
    if len(satellites) != 3:
        return jsonify({"error": "Se requieren datos de 3 satélites"}), 400
    
    try:
        # Extraer distancias y mensajes en el orden correcto
        distances = []
        messages = []
        
        for sat in satellites:
            if sat['name'] not in SATELLITES:
                return jsonify({"error": f"Satélite {sat['name']} desconocido"}), 400
                
            distances.append(float(sat['distance']))
            messages.append(sat['message'])
        
        # Calcular posición y mensaje
        x, y = get_location(distances)
        message = get_message(messages)
        
        return jsonify({
            "position": {"x": x, "y": y},
            "message": message
        }), 200
        
    except Exception as e:
        return jsonify({"error": "No se puede determinar la posición o el mensaje", "details": str(e)}), 404

# Endpoints para el Nivel 3
@app.route('/topsecret_split/<satellite_name>', methods=['POST'])
def topsecret_split_add(satellite_name):
    if satellite_name not in SATELLITES:
        return jsonify({"error": "Satélite desconocido"}), 404
    
    data = request.get_json()
    
    if not data or 'distance' not in data or 'message' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Almacenar los datos del satélite
    satellite_data[satellite_name] = {
        "distance": float(data['distance']),
        "message": data['message']
    }
    
    return jsonify({"message": "Datos recibidos"}), 200

@app.route('/topsecret_split/', methods=['GET'])
def topsecret_split_get():
    if len(satellite_data) < 3:
        return jsonify({"error": "No hay suficiente información"}), 404
    
    try:
        # Ordenar los datos: kenobi, skywalker, sato
        ordered_data = [
            satellite_data['kenobi'],
            satellite_data['skywalker'],
            satellite_data['sato']
        ]
        
        distances = [d['distance'] for d in ordered_data]
        messages = [d['message'] for d in ordered_data]
        
        x, y = get_location(distances)
        message = get_message(messages)
        
        return jsonify({
            "position": {"x": x, "y": y},
            "message": message
        }), 200
        
    except Exception as e:
        return jsonify({"error": "No se puede determinar la posición o el mensaje", "details": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
