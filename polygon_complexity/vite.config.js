import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', 
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') 
      }
    },
    port: 5173, 
    open: true 
  },
  resolve: {
    alias: {
      'katex/fonts': 'https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/fonts/'
    }
  },
})
