import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/indext.js'
import i18n from './lang/index.js'

createApp(App).use(router).use(i18n).mount('#app')