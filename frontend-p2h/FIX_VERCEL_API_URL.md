# 🔧 Fix API Base URL untuk Vercel

## Masalah

Frontend di Vercel masih memanggil `http://localhost:8000` padahal backend sudah di Railway.

Browser user **TIDAK PUNYA** localhost:8000!

## Solusi: Update Environment Variable di Vercel

### 1. Login ke Vercel Dashboard

https://vercel.com/dashboard

### 2. Pilih Project Frontend

Klik project **p2h-web** (atau nama project Vercel Anda)

### 3. Buka Settings → Environment Variables

1. Klik tab **"Settings"**
2. Scroll ke **"Environment Variables"**
3. Klik **"Add New"**

### 4. Tambahkan Variable

**Key:**

```
VITE_API_BASE_URL
```

**Value:**

```
https://p2h-web-production.up.railway.app
```

**Environments:** Pilih semua (Production, Preview, Development)

Klik **"Save"**

### 5. Redeploy

Setelah save, Vercel akan minta redeploy:

1. Klik **"Redeploy"** atau
2. Push commit baru ke GitHub untuk trigger auto-deploy

---

## ✅ Verifikasi

Setelah redeploy selesai:

1. Buka frontend Vercel di browser
2. Buka **DevTools** (F12) → **Network** tab
3. Login atau refresh page
4. Lihat request API - harus ke `https://p2h-web-production.up.railway.app`, **BUKAN** `localhost:8000`

---

## 📝 Catatan

- `.env` file **TIDAK** ter-commit ke Git (ada di `.gitignore`)
- Environment variables di Vercel **override** `.env` local
- Setiap update env variable perlu **redeploy**

---

## 🔄 Untuk Development Lokal

Jika mau test dengan backend Railway di local:

Update `.env` lokal:

```bash
VITE_API_BASE_URL=https://p2h-web-production.up.railway.app
```

Atau tetap pakai localhost jika backend jalan lokal:

```bash
VITE_API_BASE_URL=http://localhost:8000
```
