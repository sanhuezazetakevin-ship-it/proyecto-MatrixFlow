/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#F8FAFC',
        sidebar: {
          DEFAULT: '#0F172A',
          hover: '#1E293B',
          text: '#94A3B8',
          active: '#38BDF8',
        },
        primary: {
          DEFAULT: '#2563EB',
          hover: '#1D4ED8',
          light: '#EFF6FF',
        },
        accent: {
          DEFAULT: '#06B6D4',
          hover: '#0891B2',
        },
        dark: '#0F172A',
        muted: '#64748B',
      },
    },
  },
  plugins: [],
}
