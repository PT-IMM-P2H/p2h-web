# Railway Deployment Guide

## ✅ Perubahan yang Sudah Dilakukan

### 1. **main.py** - Port dan Host Configuration

- ✅ Port sekarang membaca dari environment variable `PORT` (Railway auto-inject)
- ✅ Host diubah dari `127.0.0.1` ke `0.0.0.0` (agar bisa diakses dari luar)

### 2. **Procfile** - Railway Start Command

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3. **railway.json** - Railway Configuration

- Build dengan Nixpacks
- Auto-restart on failure

## 🚀 Langkah Deploy ke Railway

### Step 1: Push ke GitHub

```bash
cd backend
git add .
git commit -m "Fix Railway deployment configuration"
git push
```

### Step 2: Railway Environment Variables

Di Railway Dashboard, tambahkan environment variables berikut:

**WAJIB:**

```
DATABASE_URL=<Railway PostgreSQL URL>
SECRET_KEY=JEShzXyadP-WP2aHeDcHdtCvpZU6F63JV9-qRps2jMW_fwrqbIgipIdZB_woGZZR84ajImfngnd18tnB3qlG8zu-rXOzJYWjOfWUhcWycQfmi3y_qMdASfu6l27sk6f3
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
APP_NAME=P2H System PT. IMM
APP_VERSION=1.0.0
ENVIRONMENT=production
```

**CORS Origins (PENTING!):**

```
CORS_ORIGINS=https://p2h-web.vercel.app,https://your-railway-app.railway.app
```

> ⚠️ Ganti `your-railway-app` dengan domain Railway Anda yang sebenarnya

**OPTIONAL (Telegram):**

```
TELEGRAM_BOT_TOKEN=8169592330:AAFgIDyHTfPi8nDorOuFZytKQPJ30uxQYF0
TELEGRAM_CHAT_ID=5625212555
```

### Step 3: Database Setup

1. Di Railway, buat PostgreSQL database
2. Copy `DATABASE_URL` dari Railway PostgreSQL
3. Paste ke environment variable `DATABASE_URL`

### Step 4: Deploy

Railway akan otomatis deploy setelah push ke GitHub.

## 🔍 Troubleshooting

### "Application failed to respond"

**Penyebab:**

- ❌ Host masih `127.0.0.1` → **SUDAH DIPERBAIKI** ke `0.0.0.0`
- ❌ Port hardcoded → **SUDAH DIPERBAIKI** pakai `$PORT`
- ⚠️ Database tidak terhubung → Cek `DATABASE_URL`
- ⚠️ Environment variables tidak di-set

**Solusi:**

1. Cek Railway logs: `Settings > Deployments > View Logs`
2. Pastikan semua environment variables sudah di-set
3. Pastikan PostgreSQL database sudah dibuat dan `DATABASE_URL` benar

### CORS Error dari Frontend

**Solusi:**
Pastikan `CORS_ORIGINS` di Railway environment variables include:

```
CORS_ORIGINS=https://p2h-web.vercel.app,https://your-backend.railway.app
```

### Database Connection Error

**Solusi:**

1. Pastikan Railway PostgreSQL sudah dibuat
2. Copy `DATABASE_URL` dari Railway PostgreSQL service
3. Format: `postgresql://user:password@host:port/database`

## 📝 Checklist Deployment

- [ ] Push code ke GitHub
- [ ] Set semua environment variables di Railway
- [ ] Buat PostgreSQL database di Railway
- [ ] Set `DATABASE_URL` dari Railway PostgreSQL
- [ ] Update `CORS_ORIGINS` dengan domain Railway backend
- [ ] Deploy dan cek logs
- [ ] Test API endpoint: `https://your-app.railway.app/`
- [ ] Test dari frontend Vercel

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
