# 🚀 CARA MUDAH SEED DATABASE PRODUCTION

## ✅ Solusi Tercepat: Gunakan Endpoint API

Saya sudah membuatkan endpoint `/admin/seed-users` yang bisa dipanggil langsung!

---

## 📋 Langkah-Langkah

### 1️⃣ Deploy Kode Terbaru ke Railway

Pastikan kode terbaru (dengan endpoint admin) sudah di-push dan deploy:

```bash
git add .
git commit -m "Add admin seed endpoint"
git push origin main
```

Railway akan otomatis deploy ulang.

### 2️⃣ Panggil Endpoint Seed

Setelah deploy selesai, panggil endpoint ini **SEKALI SAJA**:

#### Via Browser / Postman

```
POST https://p2h-web-production.up.railway.app/admin/seed-users?secret_key=IMM-P2H-SEED-2026
```

#### Via cURL (PowerShell)

```powershell
curl -X POST "https://p2h-web-production.up.railway.app/admin/seed-users?secret_key=IMM-P2H-SEED-2026"
```

#### Via Swagger UI

1. Buka: https://p2h-web-production.up.railway.app/docs
2. Cari endpoint `POST /admin/seed-users`
3. Klik "Try it out"
4. Isi `secret_key`: `IMM-P2H-SEED-2026`
5. Klik "Execute"

---

## ✅ Response Sukses

Jika berhasil, Anda akan mendapat response:

```json
{
  "status": "success",
  "message": "Users seeded successfully",
  "data": {
    "created": [
      {
        "name": "Yunnifa Nur Lailli",
        "phone": "085754538366",
        "password": "yunnifa12062003",
        "role": "superadmin"
      },
      {
        "name": "Budi Santoso",
        "phone": "081234567890",
        "password": "budi15051990",
        "role": "user"
      }
    ],
    "updated": [],
    "total": 2
  }
}
```

---

## 🔐 Login Setelah Seed

Sekarang Anda bisa login dengan:

### **Superadmin**

- **Username**: `085754538366`
- **Password**: `yunnifa12062003`

### **User Biasa**

- **Username**: `081234567890`
- **Password**: `budi15051990`

---

## 🔒 Keamanan

- Endpoint ini dilindungi dengan `secret_key`
- Secret key: `IMM-P2H-SEED-2026`
- **HANYA PANGGIL SEKALI** saat setup awal
- Jika dipanggil lagi, akan update password user yang sudah ada

---

## ⚠️ Troubleshooting

### Error 403 Forbidden

- Secret key salah
- Pastikan menggunakan: `IMM-P2H-SEED-2026`

### Error 500 Internal Server Error

- Database connection issue
- Cek Railway logs: `railway logs`

### User masih tidak bisa login

- Tunggu beberapa detik setelah seed
- Coba restart Railway service
- Cek database dengan: `railway run python check_login_credentials.py`

---

## 🎯 Next Steps

Setelah seed berhasil:

1. ✅ Test login di frontend dengan user `085754538366`
2. ✅ Verifikasi role superadmin berfungsi
3. ✅ Buat user baru via admin panel
4. ✅ **GANTI SECRET KEY** di production untuk keamanan!

---

## 🔐 Ganti Secret Key (Recommended)

Setelah seed selesai, ganti secret key di `app/routers/admin.py`:

```python
SEED_SECRET = "YOUR-NEW-SECURE-SECRET-2026"
```

Atau lebih baik, pindahkan ke environment variable:

```python
SEED_SECRET = os.getenv("ADMIN_SEED_SECRET", "default-secret")
```

Lalu set di Railway Variables:

```
ADMIN_SEED_SECRET=your-very-secure-random-string
```
