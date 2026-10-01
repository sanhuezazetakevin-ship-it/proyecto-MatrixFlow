/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          darkest: '#071014',
          darker: '#0A1F24',
          dark: '#0F3A3F',
          teal: '#1C6B6A',
          mint: '#B8F2E6',
          mintHover: '#A2EADF',
        },
        primary: {
          DEFAULT: '#1C6B6A',
          hover: '#0F3A3F',
          light: '#E6F7F5',
          dark: '#B8F2E6',
        },
        accent: {
          DEFAULT: '#B8F2E6',
          dark: '#1C6B6A',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out forwards',
        'slide-up': 'slideUp 0.4s ease-out forwards',
        'pulse-subtle': 'pulseSubtle 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
}
