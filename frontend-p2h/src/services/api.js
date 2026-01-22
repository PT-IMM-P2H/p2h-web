import axios from 'axios';
import { API_BASE_URL, API_TIMEOUT } from '../config/app.config';
import { STORAGE_KEYS, HTTP_STATUS } from '../constants';
import { logger } from '../utils/logger';

// Buat instance axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- INTERCEPTORS ---

// Request interceptor - tambahkan token JWT ke setiap request
api.interceptors.request.use(
  (config) => {
    // Add timestamp for request tracking
    config.metadata = { startTime: new Date() };
    
    const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log API request in debug mode
    logger.apiRequest(config.method, config.url, config.data || config.params);
    
    return config;
  },
  (error) => {
    logger.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor - handle responses and errors
api.interceptors.response.use(
  (response) => {
    // Calculate request duration
    const duration = new Date() - response.config.metadata.startTime;
    
    // Log API response in debug mode
    logger.apiResponse(response.config.method, response.config.url, response.data, duration);
    
    return response;
  },
  (error) => {
    // Log API error
    logger.apiError(
      error.config?.method || 'UNKNOWN',
      error.config?.url || 'UNKNOWN',
      error.response?.data || error.message
    );
    
    // Handle specific error codes
    if (error.response?.status === HTTP_STATUS.UNAUTHORIZED) {
      // Token expired atau invalid, bersihkan storage & redirect
      localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER_DATA);

      // Cek agar tidak redirect loop jika user sudah di halaman login
      if (window.location.pathname !== '/login') {
        logger.warn('Unauthorized access, redirecting to login...');
        window.location.href = '/login';
      }
    } else if (error.response?.status === HTTP_STATUS.FORBIDDEN) {
      logger.warn('Access forbidden:', error.response.data);
    } else if (error.code === 'ECONNABORTED') {
      logger.error('Request timeout:', error.config.url);
    } else if (!error.response) {
      logger.error('Network error - server may be down');
    }
    
    return Promise.reject(error);
  }
);

// --- 2. API SERVICES TERPUSAT ---
// Kita bungkus semua endpoint dalam objek agar mudah dipanggil di Component

const apiService = {
  // Akses raw axios instance jika butuh custom request
  instance: api,

  // A. AUTHENTICATION
  auth: {
    login: (credentials) => api.post('/auth/login', credentials),
    getProfile: () => api.get('/auth/me'), // Endpoint /users/me atau /auth/me sesuaikan backend
  },

  // B. MASTER DATA (CRUD)
  master: {
    // Perusahaan
    getCompanies: () => api.get('/master-data/companies'),
    createCompany: (data) => api.post('/master-data/companies', data),
    updateCompany: (id, data) => api.put(`/master-data/companies/${id}`, data),
    deleteCompany: (id) => api.delete(`/master-data/companies/${id}`),

    // Departemen
    getDepartments: () => api.get('/master-data/departments'),
    createDepartment: (data) => api.post('/master-data/departments', data),
    updateDepartment: (id, data) => api.put(`/master-data/departments/${id}`, data),
    deleteDepartment: (id) => api.delete(`/master-data/departments/${id}`),

    // Posisi
    getPositions: () => api.get('/master-data/positions'),
    createPosition: (data) => api.post('/master-data/positions', data),
    updatePosition: (id, data) => api.put(`/master-data/positions/${id}`, data),
    deletePosition: (id) => api.delete(`/master-data/positions/${id}`),

    // Status Kerja
    getStatuses: () => api.get('/master-data/work-statuses'),
    createStatus: (data) => api.post('/master-data/work-statuses', data),
    updateStatus: (id, data) => api.put(`/master-data/work-statuses/${id}`, data),
    deleteStatus: (id) => api.delete(`/master-data/work-statuses/${id}`),
  },

  // C. CHECKLIST (KELOLA PERTANYAAN)
  checklist: {
    getAll: () => api.get('/checklist'), // Admin: Semua pertanyaan
    create: (data) => api.post('/checklist', data), // Admin: Tambah
    delete: (id) => api.delete(`/checklist/${id}`), // Admin: Hapus
    // User: Mengambil checklist aktif untuk form P2H
    getActive: (vehicleType) => api.get(`/p2h/checklist/${vehicleType}`),
  },

  // D. USER MANAGEMENT
  users: {
    getAll: (params) => api.get('/users', { params }),
    getById: (id) => api.get(`/users/${id}`),
    create: (data) => api.post('/users', data),
    update: (id, data) => api.put(`/users/${id}`, data),
    delete: (id) => api.delete(`/users/${id}`), // Soft delete
  },

  // E. KENDARAAN (VEHICLES) & MONITORING
  vehicles: {
    // Ambil semua (bisa filter ?kategori_pengguna=IMM)
    getAll: (params) => api.get('/vehicles', { params }),
    // Detail per ID
    getById: (id) => api.get(`/vehicles/${id}`),
    // Cari Publik via No Lambung (P.309)
    getByLambung: (lambung) => api.get(`/vehicles/lambung/${lambung}`),
    // Create new vehicle
    create: (data) => api.post('/vehicles', data),
    // Update vehicle
    update: (id, data) => api.put(`/vehicles/${id}`, data),
    // Delete vehicle (soft delete)
    delete: (id) => api.delete(`/vehicles/${id}`),
  },

  // F. LAPORAN P2H
  p2h: {
    submit: (data) => api.post('/p2h/reports', data),
    getList: (params) => api.get('/p2h/reports', { params }),
    getDetail: (id) => api.get(`/p2h/reports/${id}`),
  }
};

// Export default apiService untuk component yang sudah diupdate
export default apiService;

// Export named api instance untuk backward compatibility
export { api };