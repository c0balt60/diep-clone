import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    base: './',
    plugins: [
        react(),
    ],
    server: {
        proxy: {
            "/ws": {
                target: "ws://127.0.0.1:8080",
                ws: true,
                changeOrigin: true
            }
        },
        //port: 8080
    }
})
