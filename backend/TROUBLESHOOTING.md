# Troubleshooting Guide - Alembic & Local Development

## ✅ Yang Sudah Diperbaiki

### 1. Railway Deployment Configuration

- ✅ Port configuration menggunakan environment variable `PORT`
- ✅ Host binding ke `0.0.0.0` untuk Railway
- ✅ `Procfile` dan `railway.json` sudah dibuat
- ✅ Code sudah di-push ke GitHub

### 2. Database Connection

- ✅ PostgreSQL berjalan di port **5432** (bukan 5433)
- ✅ `.env` sudah diupdate ke port 5432
- ✅ Database connection test berhasil

## ⚠️ Issue: Alembic Encoding Error

### Error Message

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xab in position 78: invalid start byte
```

### Penyebab

Ada karakter non-UTF-8 di salah satu file Python (kemungkinan di `app/routers/export.py` atau file lain).

### Solusi Sementara: Skip Alembic, Gunakan SQLAlchemy Langsung

**Untuk development lokal:**

```bash
# Buat tables langsung dari models (tanpa alembic)
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine); print('✅ Tables created')"
```

**Untuk Railway (Production):**
Railway akan otomatis membuat tables saat aplikasi pertama kali dijalankan karena kode di atas akan dieksekusi.

### Solusi Permanen: Fix Encoding

1. **Cari file yang bermasalah:**

```powershell
# Cek semua file Python
Get-ChildItem -Path .\app -Recurse -Filter *.py | ForEach-Object {
    try {
        Get-Content $_.FullName -Encoding UTF8 -ErrorAction Stop | Out-Null
        Write-Host "OK: $($_.FullName)"
    } catch {
        Write-Host "ERROR: $($_.FullName)" -ForegroundColor Red
    }
}
```

2. **Fix file yang error:**
   - Buka file dengan VS Code
   - Save as dengan encoding UTF-8

## 🚀 Cara Menjalankan Aplikasi Lokal

### Opsi 1: Tanpa Alembic (Recommended untuk sekarang)

```bash
# 1. Pastikan PostgreSQL running di port 5432
# 2. Create tables
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 3. Run aplikasi
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Opsi 2: Dengan Alembic (Setelah fix encoding)

```bash
# 1. Run migrations
python -m alembic upgrade head

# 2. Run aplikasi
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📋 Railway Deployment Checklist

Untuk deploy ke Railway, pastikan:

- [x] Code sudah di-push ke GitHub
- [ ] Set environment variables di Railway:
  - `DATABASE_URL` (dari Railway PostgreSQL)
  - `SECRET_KEY`
  - `CORS_ORIGINS` (include domain Railway dan Vercel)
  - `ALGORITHM=HS256`
  - `ACCESS_TOKEN_EXPIRE_MINUTES=120`
  - `APP_NAME=P2H System PT. IMM`
  - `APP_VERSION=1.0.0`
  - `ENVIRONMENT=production`
- [ ] PostgreSQL database sudah dibuat di Railway
- [ ] Check deployment logs di Railway
- [ ] Test API endpoint: `https://your-app.railway.app/`

## 🔍 Debugging Railway

### Cek Logs

```bash
# Di Railway Dashboard
Settings > Deployments > View Logs
```

### Test Endpoint

```bash
# Test root endpoint
curl https://your-app.railway.app/

# Test docs
https://your-app.railway.app/docs
```

### Common Issues

**1. "Application failed to respond"**

- ✅ FIXED: Host dan port configuration sudah benar
- Check: Database connection (pastikan `DATABASE_URL` benar)
- Check: Environment variables sudah di-set semua

**2. CORS Error**

- Pastikan `CORS_ORIGINS` include domain frontend Vercel
- Format: `https://p2h-web.vercel.app,https://your-backend.railway.app`

**3. Database Error**

- Pastikan Railway PostgreSQL sudah dibuat
- Copy `DATABASE_URL` dari Railway PostgreSQL service
- Paste ke environment variable

## 💡 Tips

1. **Untuk development lokal:** Gunakan SQLAlchemy `create_all()` instead of alembic
2. **Untuk production (Railway):** Tables akan auto-created saat startup
3. **Fix encoding error:** Bisa dilakukan nanti, tidak blocking deployment
