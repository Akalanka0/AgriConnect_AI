import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy /ask requests to the FastAPI backend during development.
      // This avoids hardcoding the backend URL in fetch calls and prevents
      // CORS preflight issues when running both servers on localhost.
      '/ask': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
