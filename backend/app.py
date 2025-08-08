import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS # Importa la extensión CORS

app = Flask(__name__)
CORS(app) # Habilita CORS para todas las rutas de la aplicación Flask

# Datos de los satélites conocidos (posición en el espacio)
SATELLITES = {
    "kenobi": {"position": [-500, -200]},
    "skywalker": {"position": [100, -100]},
    "sato": {"position": [500, 100]}
}

# Almacenamiento temporal para el endpoint /topsecret_split/
# Este diccionario guardará los datos de distancia y mensaje de cada satélite
# hasta que se reciban los tres para poder calcular la posición y el mensaje completo.
satellite_data = {}

def get_location(distances):
    """
    Calcula la posición (x, y) del emisor del mensaje mediante trilateración.
    Utiliza un sistema de ecuaciones para encontrar la intersección de las esferas
    (círculos en 2D) definidas por las distancias a cada satélite.

    Args:
        distances (list): Lista de distancias a los satélites en el orden [kenobi, skywalker, sato].

    Returns:
        tuple: Tupla (x, y) con las coordenadas del emisor.
        Raises ValueError: Si no se puede determinar la posición.
    """
    # Posiciones fijas de los satélites
    positions = [
        SATELLITES["kenobi"]["position"],
        SATELLITES["skywalker"]["position"],
        SATELLITES["sato"]["position"]
    ]
    
    # Construcción del sistema de ecuaciones lineales para trilateración
    # Se utilizan las ecuaciones de círculos: (x - xi)^2 + (y - yi)^2 = di^2
    # y se restan para linealizar el sistema.
    A = [] # Matriz de coeficientes
    b = [] # Vector de términos independientes
    
    # Se forman ecuaciones usando pares de satélites (1 vs 0, 2 vs 1, etc.)
    for i in range(1, len(positions)):
        x1, y1 = positions[i-1]
        x2, y2 = positions[i]
        d1 = distances[i-1]
        d2 = distances[i]
        
        # Ecuación linealizada: 2(x2-x1)x + 2(y2-y1)y = (x2^2 - x1^2 + y2^2 - y1^2 + d1^2 - d2^2)
        A.append([2*(x2 - x1), 2*(y2 - y1)])
        b.append(x2**2 - x1**2 + y2**2 - y1**2 + d1**2 - d2**2)
    
    # Convierte las listas a arrays de NumPy para realizar cálculos matriciales
    A = np.array(A)
    b = np.array(b)
    
    # Resuelve el sistema de ecuaciones lineales Ax = b utilizando mínimos cuadrados.
    # rcond=None es para compatibilidad con versiones futuras de NumPy.
    try:
        x, y = np.linalg.lstsq(A, b, rcond=None)[0]
    except np.linalg.LinAlgError:
        # Esto ocurre si la matriz A es singular o los datos son inconsistentes
        raise ValueError("No se pudo resolver el sistema de trilateración. Datos inconsistentes.")
        
    return float(x), float(y) # Devuelve las coordenadas como flotantes

def get_message(messages):
    """
    Reconstruye el mensaje original a partir de las versiones parciales de los satélites.
    Asume que cada satélite envía una lista de palabras, donde las palabras vacías ("")
    representan huecos en el mensaje. La primera palabra no vacía en cada posición
    se considera la palabra correcta.

    Args:
        messages (list): Lista de listas con los mensajes recibidos por cada satélite.
                         Ej: [["este", "", "", "mensaje", ""], ["", "es", "", "", "secreto"]]

    Returns:
        str: String con el mensaje reconstruido, sin espacios extra al inicio/final.
    """
    # Encuentra la longitud máxima de cualquier mensaje parcial para iterar sobre todas las posiciones de palabras
    max_len = max(len(msg) for msg in messages)
    full_message = [] # Lista para almacenar las palabras del mensaje reconstruido
    
    # Itera por cada posición de palabra en el mensaje completo
    for i in range(max_len):
        word = "" # Variable temporal para la palabra en la posición actual
        # Itera a través de los mensajes de cada satélite para encontrar la palabra en la posición 'i'
        for msg in messages:
            # Si la posición 'i' existe en el mensaje del satélite y la palabra no está vacía
            if i < len(msg) and msg[i] != "":
                word = msg[i] # Asigna la palabra no vacía
                break        # Rompe el bucle interno, ya que encontramos la palabra para esta posición
        full_message.append(word) # Añade la palabra (o vacío si no se encontró) al mensaje completo
        
    # Une todas las palabras con un espacio y elimina espacios extra al inicio/final
    return " ".join(full_message).strip()

# --- Endpoint para el Nivel 2: /topsecret/ (Decifrado en Lote) ---
@app.route('/topsecret/', methods=['POST'])
def topsecret():
    """
    Recibe la distancia y el mensaje de todos los satélites en una sola solicitud POST.
    Calcula la posición de la fuente y reconstruye el mensaje.
    """
    data = request.get_json() # Obtiene los datos JSON del cuerpo de la solicitud

    # Validaciones iniciales de los datos de entrada
    if not data or 'satellites' not in data:
        return jsonify({"error": "Datos inválidos. Se espera un JSON con 'satellites'."}), 400
    
    satellites = data['satellites']
    
    if len(satellites) != 3:
        return jsonify({"error": "Se requieren datos de 3 satélites (kenobi, skywalker, sato)."}), 400
    
    # Listas para almacenar las distancias y mensajes en el orden correcto
    # (Kenobi, Skywalker, Sato) para los cálculos de trilateración y mensaje.
    distances_ordered = [0, 0, 0] # Inicializa con ceros
    messages_ordered = ["", "", ""] # Inicializa con cadenas vacías

    # Mapeo de nombres de satélites a índices para asegurar el orden
    satellite_order_map = {"kenobi": 0, "skywalker": 1, "sato": 2}

    try:
        for sat in satellites:
            sat_name = sat.get('name')
            sat_distance = sat.get('distance')
            sat_message = sat.get('message')

            # Validar que todos los campos necesarios están presentes y correctos
            if not all([sat_name, sat_distance is not None, sat_message is not None]):
                return jsonify({"error": "Datos incompletos para un satélite. Se requiere 'name', 'distance', 'message'."}), 400
            
            if sat_name not in SATELLITES:
                return jsonify({"error": f"Satélite '{sat_name}' desconocido. Los satélites válidos son: kenobi, skywalker, sato."}), 400
            
            if not isinstance(sat_distance, (int, float)):
                return jsonify({"error": f"La distancia para '{sat_name}' debe ser un número."}), 400
            
            if not isinstance(sat_message, list):
                return jsonify({"error": f"El mensaje para '{sat_name}' debe ser una lista de palabras."}), 400

            # Almacena los datos en el orden predefinido
            index = satellite_order_map[sat_name]
            distances_ordered[index] = float(sat_distance)
            messages_ordered[index] = sat_message
            
        # Calcular posición y mensaje utilizando las funciones auxiliares
        x, y = get_location(distances_ordered)
        message = get_message(messages_ordered)
        
        # Devuelve la respuesta JSON con la posición y el mensaje
        return jsonify({
            "position": {"x": x, "y": y},
            "message": message
        }), 200
        
    except ValueError as ve:
        # Captura errores específicos de cálculo (ej. inconsistencia en trilateración)
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Captura cualquier otro error inesperado durante el procesamiento
        return jsonify({"error": "No se puede determinar la posición o el mensaje", "details": str(e)}), 404

# --- Endpoints para el Nivel 3: /topsecret_split/ (Decifrado Fragmentado) ---

@app.route('/topsecret_split/<satellite_name>', methods=['POST'])
def topsecret_split_add(satellite_name):
    """
    Recibe la distancia y el mensaje de un solo satélite y los almacena temporalmente.
    """
    # Valida si el nombre del satélite es conocido
    if satellite_name not in SATELLITES:
        return jsonify({"error": "Satélite desconocido. Los satélites válidos son: kenobi, skywalker, sato."}), 404
    
    data = request.get_json() # Obtiene los datos JSON del cuerpo de la solicitud
    
    # Valida que los datos sean completos
    if not data or 'distance' not in data or 'message' not in data:
        return jsonify({"error": "Datos incompletos. Se requiere 'distance' y 'message'."}), 400
    
    if not isinstance(data['distance'], (int, float)):
        return jsonify({"error": "La distancia debe ser un número."}), 400
    
    if not isinstance(data['message'], list):
        return jsonify({"error": "El mensaje debe ser una lista de palabras."}), 400

    # Almacenar los datos del satélite en el diccionario global 'satellite_data'
    satellite_data[satellite_name] = {
        "distance": float(data['distance']),
        "message": data['message']
    }
    
    # Devuelve un mensaje de éxito
    return jsonify({"message": f"Datos de '{satellite_name}' recibidos y almacenados."}), 200

@app.route('/topsecret_split/', methods=['GET'])
def topsecret_split_get():
    """
    Calcula la posición y reconstruye el mensaje a partir de los datos almacenados
    de los satélites, si hay suficiente información (3 satélites).
    """
    global satellite_data # Mover esta línea aquí para corregir el SyntaxError
    
    # Valida si se han recibido datos de los 3 satélites requeridos
    if len(satellite_data) < 3:
        return jsonify({"error": "No hay suficiente información. Se requieren datos de 3 satélites para descifrar."}), 404
    
    # Valida que tengamos datos para los 3 satélites específicos
    required_satellites = ["kenobi", "skywalker", "sato"]
    if not all(sat_name in satellite_data for sat_name in required_satellites):
        return jsonify({"error": "Faltan datos de uno o más satélites específicos (kenobi, skywalker, sato)."}), 404

    try:
        # Ordenar los datos de los satélites para que coincidan con el orden esperado por get_location y get_message
        ordered_data = [
            satellite_data['kenobi'],
            satellite_data['skywalker'],
            satellite_data['sato']
        ]
        
        # Extraer las distancias y los mensajes de los datos ordenados
        distances = [d['distance'] for d in ordered_data]
        messages = [d['message'] for d in ordered_data]
        
        # Calcular posición y mensaje
        x, y = get_location(distances)
        message = get_message(messages)
        
        # Limpiar los datos almacenados después de un cálculo exitoso para evitar
        # que se usen datos antiguos en futuras solicitudes GET.
        # Solo limpiar si el cálculo fue exitoso.
        satellite_data = {} 

        # Devuelve la respuesta JSON con la posición y el mensaje
        return jsonify({
            "position": {"x": x, "y": y},
            "message": message
        }), 200
        
    except ValueError as ve:
        # Captura errores específicos de cálculo
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Captura cualquier otro error inesperado
        return jsonify({"error": "No se puede determinar la posición o el mensaje", "details": str(e)}), 404

# Punto de entrada principal para ejecutar la aplicación Flask
if __name__ == '__main__':
    # app.run(debug=True) inicia el servidor de desarrollo de Flask.
    # debug=True habilita el modo de depuración, lo que proporciona recarga automática
    # y un depurador interactivo en el navegador para los errores.
    # Se ejecutará en http://127.0.0.1:5000 por defecto.
    app.run(debug=True, port=5000)