/** @type {import('tailwindcss').Config} */
module.exports = {
  // Configura Tailwind para escanear tus archivos React para las clases CSS
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Asegúrate de que esto esté presente
  ],
  theme: {
    extend: {
      // Define familias de fuentes personalizadas
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      // Define animaciones CSS personalizadas
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
      // Asigna nombres a las animaciones para usarlas con clases de Tailwind
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'fade-in-up': 'fadeInUp 0.3s ease-out forwards',
      },
    },
  },
  plugins: [], // Plugins adicionales de Tailwind (ninguno por ahora)
}