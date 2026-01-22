/**
 * Application Configuration
 * Environment-specific settings and application-wide config
 */

// Base API URL from environment variable or fallback to default
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Application Name
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'P2H System'

// Application Version
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0'

// Environment
export const ENV = import.meta.env.MODE || 'development'

// Is Production
export const IS_PRODUCTION = ENV === 'production'

// Is Development
export const IS_DEVELOPMENT = ENV === 'development'

// Debug Mode
export const DEBUG_MODE = import.meta.env.VITE_DEBUG === 'true' || IS_DEVELOPMENT

// API Timeout (in milliseconds)
export const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT) || 30000

// Token Expiry Time (in minutes)
export const TOKEN_EXPIRY = parseInt(import.meta.env.VITE_TOKEN_EXPIRY) || 30

// Refresh Token Before Expiry (in minutes)
export const REFRESH_TOKEN_BEFORE = parseInt(import.meta.env.VITE_REFRESH_TOKEN_BEFORE) || 5

// Default Language
export const DEFAULT_LANGUAGE = import.meta.env.VITE_DEFAULT_LANGUAGE || 'id'

// Supported Languages
export const SUPPORTED_LANGUAGES = ['id', 'en']

// Date/Time Settings
export const TIMEZONE = import.meta.env.VITE_TIMEZONE || 'Asia/Jakarta'

// Chart Animation Duration (ms)
export const CHART_ANIMATION_DURATION = 2000

// Toast/Notification Duration (ms)
export const NOTIFICATION_DURATION = 3000

// Max File Upload Size (in bytes) - 5MB
export const MAX_FILE_SIZE = parseInt(import.meta.env.VITE_MAX_FILE_SIZE) || 5 * 1024 * 1024

// Allowed File Types for upload
export const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']

// Feature Flags
export const FEATURES = {
  ENABLE_TELEGRAM_NOTIFICATIONS: import.meta.env.VITE_ENABLE_TELEGRAM === 'true',
  ENABLE_EMAIL_NOTIFICATIONS: import.meta.env.VITE_ENABLE_EMAIL === 'true',
  ENABLE_DARK_MODE: import.meta.env.VITE_ENABLE_DARK_MODE === 'true',
  ENABLE_MULTI_LANGUAGE: true
}

// Application Config Object
export default {
  API_BASE_URL,
  APP_NAME,
  APP_VERSION,
  ENV,
  IS_PRODUCTION,
  IS_DEVELOPMENT,
  DEBUG_MODE,
  API_TIMEOUT,
  TOKEN_EXPIRY,
  REFRESH_TOKEN_BEFORE,
  DEFAULT_LANGUAGE,
  SUPPORTED_LANGUAGES,
  TIMEZONE,
  CHART_ANIMATION_DURATION,
  NOTIFICATION_DURATION,
  MAX_FILE_SIZE,
  ALLOWED_FILE_TYPES,
  FEATURES
}
