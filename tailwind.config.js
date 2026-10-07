/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        orange: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#ff5500', // Signature vibrant orange
          600: '#ea4a00',
          700: '#c23800',
          800: '#9a2f00',
          900: '#7c2802',
          950: '#431201',
        },
        coral: {
          400: '#ff7744',
          500: '#ff5500',
          600: '#e04800',
        }
      },
      fontFamily: {
        sans: ['Sansation', 'sans-serif'],
        display: ['Sansation', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
