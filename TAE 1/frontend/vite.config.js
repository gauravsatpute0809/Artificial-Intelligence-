import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/get_departments': 'http://localhost:5000',
      '/get_doctors': 'http://localhost:5000',
      '/check_availability': 'http://localhost:5000',
      '/book_appointment': 'http://localhost:5000',
      '/chat': 'http://localhost:5000',
    }
  }
})
