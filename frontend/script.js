// Asegura que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias a elementos del DOM ---
    const modeTopsecretBtn = document.getElementById('mode-topsecret');
    const modeTopsecretSplitBtn = document.getElementById('mode-topsecret-split');
    const topsecretSection = document.getElementById('topsecret-section');
    const topsecretSplitSection = document.getElementById('topsecret-split-section');
    const resultsSection = document.getElementById('results-section');
    const resultPositionSpan = document.getElementById('result-position');
    const resultMessageSpan = document.getElementById('result-message');
    const toastContainer = document.getElementById('toast-container');

    // Elementos del formulario TopSecret (Lote)
    const topsecretForm = document.getElementById('topsecret-form');
    const kenobiDistanceInput = document.getElementById('kenobi-distance');
    const kenobiMessageInput = document.getElementById('kenobi-message');
    const skywalkerDistanceInput = document.getElementById('skywalker-distance');
    const skywalkerMessageInput = document.getElementById('skywalker-message');
    const satoDistanceInput = document.getElementById('sato-distance');
    const satoMessageInput = document.getElementById('sato-message');
    const submitTopsecretBtn = document.getElementById('submit-topsecret');

    // Elementos del formulario TopSecret Split (Fragmentado)
    const topsecretSplitForm = document.getElementById('topsecret-split-form');
    const splitSatelliteNameSelect = document.getElementById('split-satellite-name');
    const splitDistanceInput = document.getElementById('split-distance');
    const splitMessageInput = document.getElementById('split-message');
    const addSplitDataBtn = document.getElementById('add-split-data');
    const getSplitResultBtn = document.getElementById('get-split-result');

    // Elementos de estado de satélites en modo Split
    const statusKenobiLi = document.getElementById('status-kenobi');
    const statusSkywalkerLi = document.getElementById('status-skywalker');
    const statusSatoLi = document.getElementById('status-sato');

    // --- Variables de estado de la aplicación ---
    let currentMode = 'topsecret'; // Modo actual de operación
    let satelliteDataSplit = {}; // Almacena los datos de satélites para el modo split
    let isLoading = false; // Estado de carga para evitar múltiples envíos

    // --- Funciones de utilidad para la UI ---

    // Muestra u oculta secciones según el modo seleccionado
    function switchMode(mode) {
        currentMode = mode;
        if (mode === 'topsecret') {
            topsecretSection.classList.remove('hidden');
            topsecretSection.classList.add('active');
            topsecretSplitSection.classList.add('hidden');
            topsecretSplitSection.classList.remove('active');
            modeTopsecretBtn.classList.add('active');
            modeTopsecretSplitBtn.classList.remove('active');
        } else {
            topsecretSection.classList.add('hidden');
            topsecretSection.classList.remove('active');
            topsecretSplitSection.classList.remove('hidden');
            topsecretSplitSection.classList.add('active');
            modeTopsecretBtn.classList.remove('active');
            modeTopsecretSplitBtn.classList.add('active');
        }
        // Limpiar resultados y estados al cambiar de modo
        displayResults(null, null);
        satelliteDataSplit = {};
        updateSplitStatusUI();
    }

    // Muestra un mensaje de notificación (toast)
    function showToast(message, type = 'success') {
        const toastDiv = document.createElement('div');
        toastDiv.classList.add('toast-message');
        toastDiv.classList.add(type); // Añade clase 'success' o 'error'
        toastDiv.innerHTML = `<span>${type === 'success' ? '✅' : '❌'}</span><p>${message}</p>`;
        
        toastContainer.appendChild(toastDiv);

        // Hace que el toast desaparezca después de 3 segundos
        setTimeout(() => {
            toastDiv.style.opacity = '0';
            toastDiv.style.transform = 'translateY(50px) translateX(-50%)'; // Desliza hacia abajo
            setTimeout(() => {
                toastDiv.remove(); // Elimina el toast del DOM
            }, 500); // Espera a que termine la animación de fade out
        }, 3000);
    }

    // Actualiza el texto y el icono del botón de envío
    function setButtonLoading(button, loading) {
        isLoading = loading;
        button.disabled = loading;
        if (loading) {
            button.classList.add('loading');
        } else {
            button.classList.remove('loading');
        }
    }

    // Muestra los resultados en la sección de resultados
    function displayResults(position, message) {
        if (position || message) {
            resultPositionSpan.textContent = position ? `X: ${position.x.toFixed(2)}, Y: ${position.y.toFixed(2)}` : 'N/A';
            resultMessageSpan.textContent = message || 'N/A';
            resultsSection.classList.remove('hidden');
        } else {
            resultsSection.classList.add('hidden');
            resultPositionSpan.textContent = '';
            resultMessageSpan.textContent = '';
        }
    }

    // Actualiza la UI de estado para el modo split
    function updateSplitStatusUI() {
        const satellites = [
            { name: 'kenobi', element: statusKenobiLi },
            { name: 'skywalker', element: statusSkywalkerLi },
            { name: 'sato', element: statusSatoLi }
        ];

        let allReceived = true;
        satellites.forEach(sat => {
            const icon = sat.element.querySelector('i');
            // Elimina clases anteriores para evitar conflictos
            icon.classList.remove('fa-check-circle', 'status-icon-ok', 'fa-times-circle', 'status-icon-fail');
            sat.element.classList.remove('status-success', 'status-error');

            if (satelliteDataSplit[sat.name]) {
                icon.classList.add('fa-check-circle', 'status-icon-ok');
                sat.element.innerHTML = `<i class="fas fa-check-circle status-icon-ok"></i> ${sat.name.charAt(0).toUpperCase() + sat.name.slice(1)}: Datos recibidos`;
                sat.element.classList.add('status-success');
            } else {
                icon.classList.add('fa-times-circle', 'status-icon-fail');
                sat.element.innerHTML = `<i class="fas fa-times-circle status-icon-fail"></i> ${sat.name.charAt(0).toUpperCase() + sat.name.slice(1)}: Esperando datos`;
                sat.element.classList.add('status-error');
                allReceived = false;
            }
        });

        // Habilita/deshabilita el botón de "Obtener Mensaje Final"
        if (allReceived) {
            getSplitResultBtn.disabled = false;
            getSplitResultBtn.classList.remove('disabled');
        } else {
            getSplitResultBtn.disabled = true;
            getSplitResultBtn.classList.add('disabled');
        }
    }

    // --- Inicialización de Partículas (Estilo Galaxia/Espacio) ---
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 250, // Muchas estrellas para una galaxia densa
                "density": {
                    "enable": true,
                    "value_area": 1200 // Esparcidas en un área grande
                }
            },
            "color": {
                // Colores para simular variedad de estrellas y quizás planetas más grandes
                "value": ["#F0F0F0", "#D0D0FF", "#FFAAAA", "#C0C0C0", "#FFD700"] // Blanco, azul pálido, rojo suave, gris, oro (para "planetas")
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                }
            },
            "opacity": {
                "value": 0.7,
                "random": true, // Opacidad aleatoria para un efecto de "parpadeo" de estrellas
                "anim": {
                    "enable": false
                }
            },
            "size": {
                "value": { min: 0.8, max: 4 }, // Rango de tamaño para estrellas y algunos "cuerpos celestes" más grandes
                "random": true, // Tamaños aleatorios para variedad
                "anim": {
                    "enable": false
                }
            },
            "line_linked": {
                "enable": false // Sin líneas para un look más de espacio abierto
            },
            "move": {
                "enable": true,
                "speed": 0.2, // Movimiento muy lento para una deriva galáctica
                "direction": "none",
                "random": true, // Movimiento aleatorio en todas direcciones
                "straight": false,
                "out_mode": "out", // Las partículas salen de la pantalla
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "bubble" // Un efecto de "burbuja" al pasar el mouse, para resaltar estrellas
                },
                "onclick": {
                    "enable": true,
                    "mode": "push" // Empuja partículas al hacer clic
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 400,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 150, // Distancia del efecto burbuja
                    "size": 6, // Tamaño de las partículas en el efecto burbuja
                    "duration": 2,
                    "opacity": 1,
                    "speed": 3
                },
                "repulse": {
                    "distance": 100,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });


    // --- Lógica de la API y Manejo de Eventos ---

    // Maneja el envío del formulario para el modo TopSecret (Lote)
    topsecretForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Evita que la página se recargue
        if (isLoading) return; // Evita envíos múltiples

        setButtonLoading(submitTopsecretBtn, true); // Activa el estado de carga del botón
        displayResults(null, null); // Limpia resultados anteriores

        const satellites = [
            { name: "kenobi", distance: parseFloat(kenobiDistanceInput.value), message: kenobiMessageInput.value.split(' ') },
            { name: "skywalker", distance: parseFloat(skywalkerDistanceInput.value), message: skywalkerMessageInput.value.split(' ') },
            { name: "sato", distance: parseFloat(satoDistanceInput.value), message: satoMessageInput.value.split(' ') }
        ];

        const payload = { satellites: satellites };

        try {
            const response = await fetch('http://127.0.0.1:5000/topsecret/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al descifrar el mensaje.');
            }

            const data = await response.json();
            displayResults(data.position, data.message); // Muestra los resultados
            showToast('¡Mensaje descifrado con éxito!', 'success');
        } catch (error) {
            console.error('Error al enviar datos topsecret:', error);
            showToast(`Error: ${error.message}`, 'error');
            displayResults(null, null);
        } finally {
            setButtonLoading(submitTopsecretBtn, false); // Desactiva el estado de carga
        }
    });

    // Maneja el envío de datos de un solo satélite para el modo Split
    topsecretSplitForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (isLoading) return;

        setButtonLoading(addSplitDataBtn, true);
        displayResults(null, null);

        const satelliteName = splitSatelliteNameSelect.value;
        const distance = parseFloat(splitDistanceInput.value);
        const message = splitMessageInput.value.split(' ');

        const payload = { distance: distance, message: message };

        try {
            const response = await fetch(`http://127.0.0.1:5000/topsecret_split/${satelliteName}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al enviar datos del satélite.');
            }

            // Actualiza el estado local de los datos split
            satelliteDataSplit[satelliteName] = { distance, message };
            updateSplitStatusUI(); // Refresca la UI de estado

            showToast(`Datos de ${satelliteName.charAt(0).toUpperCase() + satelliteName.slice(1)} recibidos.`, 'success');

            // Limpia los campos de entrada
            splitDistanceInput.value = '';
            splitMessageInput.value = '';

        } catch (error) {
            console.error('Error al enviar datos split:', error);
            showToast(`Error: ${error.message}`, 'error');
            displayResults(null, null);
        } finally {
            setButtonLoading(addSplitDataBtn, false);
        }
    });

    // Maneja la solicitud para obtener el resultado final en modo Split
    getSplitResultBtn.addEventListener('click', async () => {
        if (isLoading || Object.keys(satelliteDataSplit).length < 3) return; // Asegura que los 3 satélites tengan datos

        setButtonLoading(getSplitResultBtn, true);
        displayResults(null, null);

        try {
            const response = await fetch('http://127.0.0.1:5000/topsecret_split/', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'No hay suficiente información para descifrar.');
            }

            const data = await response.json();
            displayResults(data.position, data.message);
            showToast('¡Mensaje final descifrado!', 'success');
            
            // Limpia los datos almacenados después de un descifrado exitoso
            satelliteDataSplit = {};
            updateSplitStatusUI();

        } catch (error) {
            console.error('Error al obtener resultado split:', error);
            showToast(`Error: ${error.message}`, 'error');
            displayResults(null, null);
        } finally {
            setButtonLoading(getSplitResultBtn, false);
        }
    });

    // --- Event Listeners para cambiar de modo ---
    modeTopsecretBtn.addEventListener('click', () => switchMode('topsecret'));
    modeTopsecretSplitBtn.addEventListener('click', () => switchMode('topsecret-split'));

    // --- Inicialización al cargar la página ---
    switchMode('topsecret'); // Inicia en el modo "Decifrar en Lote" por defecto
    updateSplitStatusUI(); // Asegura que el estado inicial del botón split sea correcto
});
