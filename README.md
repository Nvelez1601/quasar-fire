# 🛰️ Quasar Fire

¡Bienvenido al Quasar Fire! Esta aplicación te permite descifrar mensajes y localizar la posición de una fuente de señal basándose en datos recibidos de múltiples satélites, utilizando algoritmos de trilateración y reconstrucción de mensajes.

![img](https://i.imgur.com/wMZ5Hjt.png)

![img](https://i.imgur.com/HQ0khcV.png)

La aplicación ofrece dos modos principales:
* **Decifrado en Lote (`/topsecret`):** Envía todos los datos de los satélites en una sola solicitud.
* **Decifrado Fragmentado (`/topsecret_split`):** Envía los datos de cada satélite individualmente y luego solicita el descifrado final.

---

## 🌟 Características

* **Detección de Posición:** Utiliza el algoritmo de trilateración para calcular las coordenadas $(x, y)$ de la fuente de la señal.
* **Descifrado de Mensajes:** Reconstruye el mensaje original a partir de fragmentos parciales recibidos por diferentes satélites.
* **Interfaz Interactiva:** Un frontend moderno y llamativo construido con React y Tailwind CSS.
* **Modos de Operación:** Soporte para ambos endpoints, `topsecret` y `topsecret_split`, permitiendo flexibilidad en el envío de datos.
* **Efectos Visuales:** Animaciones de carga, notificaciones *toast* y un relajante fondo de partículas.
* **Diseño Profesional:** Interfaz limpia, minimalista y con iconos alusivos.

---

## 🛠️ Tecnologías Utilizadas

### Backend (API REST)
* **Python 🐍:** Lenguaje de programación.
* **Flask 🌐:** Microframework web para construir la API REST.
* **NumPy ✨:** Librería para cálculos numéricos (utilizada en la trilateración).
* **Flask-CORS 🔗:** Extensión para manejar las políticas de *Cross-Origin Resource Sharing* (CORS), permitiendo la comunicación con el frontend.

### Frontend (Interfaz de Usuario)
* **HTML5 📄:** Estructura de la página web.
* **JavaScript (ES6+) 💻:** Lógica interactiva, manejo de la API y control de la interfaz.
* **CSS3 🎨:** Estilos y efectos visuales, incluyendo animaciones y un diseño responsivo, con una paleta de colores Star Wars.
* **`Particles.js`  💫:** Librería para generar el fondo interactivo de partículas (estilo galaxia).

---
## 🚀 Cómo Empezar

Para poner en marcha este proyecto, necesitas configurar tanto el backend de Flask como el frontend de React.

### Configuración del Backend (Flask)

1.  **Clona este repositorio (si aplica) o guarda el código:**
    Guarda el código de tu API de Flask (el archivo `app.py` que me proporcionaste) en una carpeta.

2.  **Crea un entorno virtual (opcional pero recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instala las dependencias de Python:**
    Asegúrate de tener `pip` actualizado y luego instala las librerías necesarias:
    ```bash
    pip install Flask numpy Flask-Cors
    ```

5.  **Ejecuta el servidor Flask:**
    Desde el directorio donde guardaste `app.py`:
    ```bash
    python app.py
    ```
    Verás un mensaje en tu terminal indicando que el servidor está corriendo, generalmente en `http://127.0.0.1:5000`.

---


## 🧪 Pruebas del Backend (con `curl`)

Mientras tu servidor Flask está corriendo, puedes probar los endpoints usando `curl` en una **tercera terminal**.

### Prueba del Endpoint `/topsecret/` (Lote)

Envía todos los datos de los satélites en una sola solicitud POST:

```bash
curl -X POST \
  [http://127.0.0.1:5000/topsecret/](http://127.0.0.1:5000/topsecret/) \
  -H 'Content-Type: application/json' \
  -d '{
    "satellites": [
      {
        "name": "kenobi",
        "distance": 100.0,
        "message": ["este", "", "", "mensaje", ""]
      },
      {
        "name": "skywalker",
        "distance": 115.5,
        "message": ["", "es", "", "", "secreto"]
      },
      {
        "name": "sato",
        "distance": 142.7,
        "message": ["este", "", "un", "", ""]
      }
    ]
  }'
