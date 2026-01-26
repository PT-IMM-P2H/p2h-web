import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // Tambahan penting untuk mengatasi warning "eval" / CSP
      'vue-i18n': 'vue-i18n/dist/vue-i18n.cjs.prod.js',
    },
  },
})