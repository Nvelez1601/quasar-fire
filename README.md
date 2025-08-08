# 🛰️ Sistema de Detección Galáctica

¡Bienvenido al Sistema de Detección Galáctica! Esta aplicación te permite descifrar mensajes y localizar la posición de una fuente de señal basándose en datos recibidos de múltiples satélites, utilizando algoritmos de trilateración y reconstrucción de mensajes.

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
* **React ⚛️:** Librería de JavaScript para construir interfaces de usuario interactivas.
* **Tailwind CSS 🎨:** Framework CSS para un desarrollo rápido y un diseño altamente personalizable y responsivo.
* **Lucide React 💡:** Colección de iconos modernos y ligeros.
* **`react-particles` / `tsparticles-slim` 💫:** Librerías para generar el fondo interactivo de partículas.

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

### Configuración del Frontend (React)

1.  **Crea un nuevo proyecto React (si no lo tienes ya):**
    Abre una **nueva terminal** (diferente a la que corre Flask) y ejecuta:
    ```bash
    npx create-react-app fiverr-space-comm-frontend
    cd fiverr-space-comm-frontend
    ```

2.  **Instala las dependencias de Node.js:**
    Necesitarás Tailwind CSS, Lucide React y las librerías de partículas.
    ```bash
    npm install -D tailwindcss postcss autoprefixer
    npm install lucide-react tsparticles tsparticles-slim react-particles
    ```
    (Si usas `yarn`, reemplaza `npm install` por `yarn add`).

3.  **Configura Tailwind CSS:**
    * **Inicializa Tailwind:**
        ```bash
        npx tailwindcss init -p
        ```
    * **Modifica `tailwind.config.js`:**
        Abre `tailwind.config.js` y asegúrate de que el `content` incluya los archivos de tu proyecto React:
        ```javascript
        /** @type {import('tailwindcss').Config} */
        module.exports = {
          content: [
            "./src/**/*.{js,jsx,ts,tsx}",
          ],
          theme: {
            extend: {
              fontFamily: {
                inter: ['Inter', 'sans-serif'],
              },
              keyframes: {
                fadeIn: {
                  '0%': { opacity: '0', transform: 'translateY(20px)' },
                  '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                fadeInUp: {
                  '0%': { opacity: '0', transform: 'translateY(20px)' },
                  '100%': { opacity: '1', transform: 'translateY(0)' },
                },
              },
              animation: {
                'fade-in': 'fadeIn 0.5s ease-out forwards',
                'fade-in-up': 'fadeInUp 0.3s ease-out forwards',
              },
            },
          },
          plugins: [],
        }
        ```
    * **Añade las directivas de Tailwind en `src/index.css`:**
        Abre `src/index.css` (o crea uno si no existe) y añade lo siguiente al principio:
        ```css
        @tailwind base;
        @tailwind components;
        @tailwind utilities;

        @import url('[https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap)');

        body {
          margin: 0;
          font-family: 'Inter', sans-serif;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }
        ```

4.  **Copia el código de la aplicación React:**
    Reemplaza el contenido de `src/App.js` con el código proporcionado en la última respuesta.

5.  **Asegúrate de que `public/index.html` tenga un `<div id="root"></div>`:**
    El archivo `public/index.html` de tu proyecto React debe contener un `div` con `id="root"`. Aquí es donde se montará tu aplicación.

6.  **Inicia la aplicación React:**
    Desde la raíz de tu proyecto React (donde está `package.json`):
    ```bash
    npm start
    ```
    Esto abrirá la aplicación en tu navegador, generalmente en `http://localhost:3000`.

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
