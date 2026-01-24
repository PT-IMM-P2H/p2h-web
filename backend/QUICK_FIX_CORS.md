# ⚡ Quick Fix CORS - Copy Paste Ready

## 🔴 Masalah

CORS error masih ada karena backend Railway belum allow domain Vercel.

---

## ✅ Solusi Cepat (1 Menit)

### Di Railway Backend Dashboard:

1. **Login:** https://railway.app/dashboard
2. **Pilih backend project** (yang ada FastAPI)
3. **Tab "Variables"**
4. **Add/Edit variable:**

**Variable Name:**

```
CORS_ORIGINS
```

**Value (Copy paste ini):**

```json
[
  "http://localhost:5173",
  "https://p2h-web.vercel.app",
  "https://p2h-web-qzc6.vercel.app",
  "https://*.vercel.app"
]
```

Atau untuk testing cepat, pakai wildcard:

```
*
```

5. **Save**
6. **Tunggu backend redeploy** (~2 menit)

---

## 🔍 Cek Backend Status

Sebelum update CORS, pastikan backend jalan:

**Buka di browser:**

```
https://p2h-api-production.up.railway.app/
```

**Expected:** JSON response

```json
{
  "status": "success",
  "message": "Welcome to P2H System PT. IMM API",
  ...
}
```

**Jika 502 atau error:** Backend crash, cek logs di Railway.

---

## 🐛 Jika Backend Crash

Di Railway backend project:

1. Tab **"Logs"**
2. Cari error messages
3. Common issues:
   - Alembic migration failed
   - Database connection timeout
   - Missing dependencies

**Quick fix:** Restart deployment

- Tab "Deployments"
- Klik deployment terakhir
- Klik "⋯" → "Redeploy"

---

## ⏱️ Timeline

1. Update CORS variable: 30 detik
2. Backend redeploy: 1-2 menit
3. Test: 30 detik

**Setelah backend redeploy selesai, refresh Vercel frontend dan test login!**
