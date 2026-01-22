/**
 * Application-wide constants
 * Centralized configuration for magic numbers, status values, and other constants
 */

// API Response Status
export const API_STATUS = {
  SUCCESS: 'success',
  ERROR: 'error',
  PENDING: 'pending'
}

// P2H Status
export const P2H_STATUS = {
  NORMAL: 'normal',
  ABNORMAL: 'abnormal',
  WARNING: 'warning'
}

// User Roles
export const USER_ROLES = {
  SUPERADMIN: 'superadmin',
  ADMIN: 'admin_monitor',
  USER: 'karyawan'
}

// User Kategori
export const USER_KATEGORI = {
  IMM: 'IMM',
  TRAVEL: 'Travel'
}

// Vehicle Types (sesuai dengan backend enum)
export const VEHICLE_TYPES = {
  LIGHT_VEHICLE: 'Light Vehicle',
  HEAVY_VEHICLE: 'Heavy Vehicle',
  ELECTRIC_VEHICLE: 'Electric Vehicle',
  BUS: 'Bus',
  MINI_BUS: 'Mini Bus'
}

// Chart Colors
export const CHART_COLORS = {
  NORMAL: {
    PRIMARY: '#10B981',
    RGB: 'rgba(16, 185, 129, 0.7)',
    RGB_LIGHT: 'rgba(16, 185, 129, 0.08)'
  },
  ABNORMAL: {
    PRIMARY: '#F59E0B',
    RGB: 'rgba(245, 158, 11, 0.7)',
    RGB_LIGHT: 'rgba(245, 158, 11, 0.08)'
  },
  WARNING: {
    PRIMARY: '#EF4444',
    RGB: 'rgba(239, 68, 68, 0.7)',
    RGB_LIGHT: 'rgba(239, 68, 68, 0.08)'
  }
}

// Date Formats
export const DATE_FORMATS = {
  ISO: 'YYYY-MM-DD',
  MONTH: 'YYYY-MM',
  DISPLAY: 'DD/MM/YYYY',
  DATETIME: 'DD/MM/YYYY HH:mm'
}

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
}

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
  LANGUAGE: 'app_language',
  THEME: 'app_theme'
}

// API Endpoints (relative paths)
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    PROFILE: '/auth/profile'
  },
  DASHBOARD: {
    STATISTICS: '/dashboard/statistics',
    MONTHLY_REPORTS: '/dashboard/monthly-reports',
    VEHICLE_TYPES: '/dashboard/vehicle-types',
    VEHICLE_TYPE_STATUS: '/dashboard/vehicle-type-status'
  },
  P2H: {
    CHECKLIST_ITEMS: '/p2h/checklist-items',
    CHECKLIST: '/p2h/checklist',
    SUBMIT: '/p2h/submit'
  },
  VEHICLES: {
    LIST: '/vehicles',
    DETAIL: '/vehicles/:id'
  },
  USERS: {
    LIST: '/users',
    DETAIL: '/users/:id'
  }
}

// Month Names (Indonesian)
export const MONTH_NAMES_ID = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]

// Month Names (English)
export const MONTH_NAMES_EN = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500
}

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Terjadi kesalahan jaringan. Silakan coba lagi.',
  UNAUTHORIZED: 'Sesi Anda telah berakhir. Silakan login kembali.',
  FORBIDDEN: 'Anda tidak memiliki akses untuk melakukan tindakan ini.',
  NOT_FOUND: 'Data tidak ditemukan.',
  INTERNAL_ERROR: 'Terjadi kesalahan pada server. Silakan hubungi administrator.'
}

export default {
  API_STATUS,
  P2H_STATUS,
  USER_ROLES,
  USER_KATEGORI,
  VEHICLE_TYPES,
  CHART_COLORS,
  DATE_FORMATS,
  PAGINATION,
  STORAGE_KEYS,
  API_ENDPOINTS,
  MONTH_NAMES_ID,
  MONTH_NAMES_EN,
  HTTP_STATUS,
  ERROR_MESSAGES
}
