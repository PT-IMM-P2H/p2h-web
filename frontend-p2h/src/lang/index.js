import { createI18n } from 'vue-i18n'
import en from './en.js'
import id from './id.js'

const messages = {
  en,
  id,
}

const i18n = createI18n({
  legacy: false,
  locale: 'id', // bahasa default
  fallbackLocale: 'en',
  messages,
})

export default i18n