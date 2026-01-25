# 🔧 Update CORS Backend Railway - URGENT

## ✅ Progress

URL sudah benar! Vercel sekarang memanggil:

```
✅ https://p2h-api-production.up.railway.app/auth/login
```

Tapi ada **CORS error** karena backend belum allow domain Vercel.

---

## 🚨 Fix CORS di Railway Backend (2 Menit)

### Step 1: Login ke Railway

Buka: **https://railway.app/dashboard**

### Step 2: Pilih Backend Project

Klik project **backend** (bukan frontend)

Biasanya nama: `p2h-web` atau `backend` atau yang ada FastAPI

### Step 3: Buka Variables Tab

Klik tab **"Variables"** di bagian atas

### Step 4: Edit CORS_ORIGINS

#### Opsi A: Cari Variable CORS_ORIGINS

Jika sudah ada variable `CORS_ORIGINS`:

1. Klik **Edit** (ikon pensil)
2. Update value menjadi:
   ```json
   [
     "http://localhost:5173",
     "https://p2h-bro0xl7kq-naufals-projects-6b92b323.vercel.app"
   ]
   ```
3. Klik **Save**

#### Opsi B: Tambah Variable Baru

Jika belum ada:

1. Klik **"New Variable"**
2. **Variable Name:** `CORS_ORIGINS`
3. **Value:**
   ```json
   [
     "http://localhost:5173",
     "https://p2h-bro0xl7kq-naufals-projects-6b92b323.vercel.app"
   ]
   ```
4. Klik **"Add"**

#### Opsi C: Sementara Allow All (untuk testing)

Untuk testing cepat, bisa set:

**Variable Name:** `CORS_ORIGINS`  
**Value:** `*`

⚠️ **WARNING:** `*` allow semua domain, **JANGAN** pakai di production final!

### Step 5: Tunggu Redeploy

Setelah save variable, Railway akan **auto-redeploy** backend.

1. Klik tab **"Deployments"**
2. Tunggu deployment terbaru sampai status **"Success"** (1-2 menit)

---

## ✅ Verifikasi

### 1. Tunggu Backend Redeploy Selesai

Di Railway Deployments tab, tunggu sampai ✅ Success.

### 2. Test dari Vercel

1. Buka **https://p2h-web.vercel.app**
2. **Ctrl+Shift+R** (hard refresh)
3. Coba **login**

### 3. Cek Console

**✅ SUKSES jika:**

- Tidak ada CORS error
- Login berhasil atau dapat response dari API
- Network tab menunjukkan status 200 atau 401 (bukan ERR_FAILED)

**❌ MASIH ERROR jika:**

- Masih ada CORS error → cek CORS_ORIGINS value
- ERR_FAILED → backend mungkin crash, cek logs

---

## 🔍 Cek Backend Logs (Jika Masih Error)

Di Railway backend project:

1. Klik tab **"Logs"**
2. Lihat error messages
3. Cari error terkait CORS atau startup

Common issues:

- Alembic migration failed
- Database connection error
- Import error

---

## 📝 Format CORS_ORIGINS yang Benar

Backend menggunakan JSON array, jadi format harus:

**✅ BENAR:**

```json
[
  "http://localhost:5173",
  "https://p2h-bro0xl7kq-naufals-projects-6b92b323.vercel.app"
]
```

**❌ SALAH:**

```
http://localhost:5173,https://p2h-web.vercel.app
```

**❌ SALAH:**

```json
[
  "http://localhost:5173",
  "https://p2h-bro0xl7kq-naufals-projects-6b92b323.vercel.app"
]
```

Harus pakai **double quotes** `"`, bukan single quotes `'`.

---

## 🎯 Summary

| Step                    | Status                    |
| ----------------------- | ------------------------- |
| Update Vercel env var   | ✅ Done                   |
| Vercel redeploy         | ✅ Done                   |
| URL sudah benar         | ✅ Done                   |
| **Update backend CORS** | ⏳ **DO THIS NOW**        |
| Backend redeploy        | ⏳ After CORS update      |
| Test login              | ⏳ After backend redeploy |

---

## ⏱️ Timeline

1. **Update CORS variable:** 30 detik
2. **Backend redeploy:** 1-2 menit
3. **Test:** 30 detik

**Total:** ~3 menit

Setelah ini, aplikasi seharusnya **100% jalan**! 🚀
