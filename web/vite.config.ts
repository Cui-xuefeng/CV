import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/local': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})
