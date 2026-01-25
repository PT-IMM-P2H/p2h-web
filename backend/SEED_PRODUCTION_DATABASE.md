# 🌱 Seed Production Database - Railway

## ❌ Masalah

User `085754538366` tidak ditemukan di database production karena **database belum di-seed**.

## ✅ Solusi: Seed Database Production

### **Opsi 1: Via Railway CLI** (Recommended)

#### 1️⃣ Install Railway CLI

```bash
# Windows (via npm)
npm install -g @railway/cli

# Atau via PowerShell
iwr https://railway.app/install.ps1 | iex
```

#### 2️⃣ Login ke Railway

```bash
railway login
```

#### 3️⃣ Link ke Project

```bash
cd e:\Magang\Github-P2H-web\p2h-web\backend
railway link
```

Pilih project **p2h-api-production**

#### 4️⃣ Run Seed Script

```bash
railway run python app/seeds/seed_users.py
```

---

### **Opsi 2: Via Railway Dashboard** (Manual)

#### 1️⃣ Buka Railway Dashboard

- Masuk ke https://railway.app
- Pilih project **p2h-api-production**
- Klik tab **"Variables"**

#### 2️⃣ Copy Environment Variables

Copy semua environment variables (terutama `DATABASE_URL`)

#### 3️⃣ Run Seed Locally dengan Production DB

```bash
# Set environment variable sementara
$env:DATABASE_URL="postgresql://..."  # paste dari Railway

# Run seed
python app/seeds/seed_users.py
```

> ⚠️ **HATI-HATI**: Ini akan langsung mengubah database production!

---

### **Opsi 3: Tambahkan Endpoint Seed** (Paling Mudah)

Saya akan buatkan endpoint API untuk seed database yang bisa dipanggil sekali.

---

## 📋 Data User yang Akan Di-Seed

Setelah seed berhasil, user berikut akan tersedia:

### **Superadmin**

- **Username**: `085754538366`
- **Password**: `yunnifa12062003`
- **Nama**: Yunnifa Nur Lailli
- **Role**: Superadmin

### **User Biasa**

- **Username**: `081234567890`
- **Password**: `budi15051990`
- **Nama**: Budi Santoso
- **Role**: User

---

## 🔐 Format Password

Password mengikuti format: **`namadepan` + `DDMMYYYY`**

Contoh:

- Yunnifa lahir 12/06/2003 → `yunnifa12062003`
- Budi lahir 15/05/1990 → `budi15051990`

---

## ✅ Verifikasi Setelah Seed

Cek apakah user sudah ada di database:

```bash
railway run python check_login_credentials.py
```

Atau test login via API:

```bash
curl -X POST https://p2h-web-production.up.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "085754538366", "password": "yunnifa12062003"}'
```

---

## 🚀 Rekomendasi Saya

**Gunakan Opsi 3** - Saya akan buatkan endpoint seed yang aman dan mudah digunakan!
