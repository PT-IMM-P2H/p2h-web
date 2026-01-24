# 🔴 CRITICAL: Railway Service URLs

## ⚠️ Railway Punya 2 Service Berbeda!

Jika Anda deploy frontend DAN backend ke Railway, akan ada **2 service dengan URL berbeda**:

### 1. Frontend Service (Static Site)

```
https://p2h-web-production.up.railway.app
```

- Ini untuk **serve HTML/CSS/JS** frontend
- **BUKAN** API endpoint!
- User akses ini di browser untuk buka aplikasi

### 2. Backend API Service (FastAPI)

```
https://p2h-api-production.up.railway.app
```

- Ini **API endpoint** yang sebenarnya
- Frontend **WAJIB** pakai URL ini untuk API calls
- Endpoint: `/auth/login`, `/p2h/reports`, dll.

---

## 🔥 Kesalahan yang Sering Terjadi

❌ **SALAH:**

```javascript
// Frontend memanggil frontend service sebagai API
const API_URL = "https://p2h-web-production.up.railway.app";
axios.get(`${API_URL}/p2h/reports`); // ❌ 502 Bad Gateway!
```

✅ **BENAR:**

```javascript
// Frontend memanggil backend API service
const API_URL = "https://p2h-api-production.up.railway.app";
axios.get(`${API_URL}/p2h/reports`); // ✅ Works!
```

---

## 📝 Update Environment Variable

### Di Vercel (untuk frontend Vercel)

**Variable:**

```
VITE_API_BASE_URL=https://p2h-api-production.up.railway.app
```

**BUKAN:**

```
VITE_API_BASE_URL=https://p2h-web-production.up.railway.app  ❌
```

### Di Railway Frontend Service (jika deploy frontend di Railway)

Sama, set environment variable:

```
VITE_API_BASE_URL=https://p2h-api-production.up.railway.app
```

---

## 🔍 Cara Cek URL yang Benar

### Di Railway Dashboard:

1. **Backend API Service:**
   - Buka project backend
   - Tab "Settings" → "Domains"
   - Copy domain (contoh: `p2h-api-production.up.railway.app`)
   - Ini yang dipakai untuk `VITE_API_BASE_URL`

2. **Frontend Service:**
   - Buka project frontend
   - Tab "Settings" → "Domains"
   - Copy domain (contoh: `p2h-web-production.up.railway.app`)
   - Ini yang user buka di browser

---

## ✅ Verifikasi

Test backend API langsung di browser:

```
https://p2h-api-production.up.railway.app/
```

Harus return JSON response dari FastAPI, bukan HTML!

```json
{
  "status": "success",
  "message": "Welcome to P2H System PT. IMM API",
  "payload": {
    "version": "1.0.0",
    "docs": "/docs"
  }
}
```

---

## 🎯 Architecture

```
[User Browser]
      |
      | Akses: https://p2h-web-production.up.railway.app
      | (atau https://p2h-web.vercel.app)
      v
[Frontend Service - HTML/CSS/JS]
      |
      | API Calls: https://p2h-api-production.up.railway.app
      v
[Backend API Service - FastAPI]
      |
      v
[Database]
```
