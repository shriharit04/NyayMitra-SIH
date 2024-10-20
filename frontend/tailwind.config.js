/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fgreen : '#0f0',
        forange : '#FB923C',
        primary: '#064635',
        secondary: '#080808',
        purp : '#190D2E'
      }
    },
  },
  plugins: [],
}