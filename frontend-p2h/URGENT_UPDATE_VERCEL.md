# 🚨 URGENT: Update Vercel Environment Variable

## Masalah Saat Ini

Vercel frontend **MASIH** memanggil URL yang salah:

```
❌ https://p2h-web-production.up.railway.app/p2h/reports
```

Seharusnya:

```
✅ https://p2h-api-production.up.railway.app/p2h/reports
```

**Penyebab:** Environment variable di Vercel belum diset/diupdate.

---

## 📝 Langkah-langkah Fix (5 Menit)

### Step 1: Login ke Vercel

Buka: **https://vercel.com/dashboard**

### Step 2: Pilih Project

Klik project frontend Anda (biasanya nama: `p2h-web` atau sejenisnya)

### Step 3: Buka Settings

1. Klik tab **"Settings"** (di bagian atas)
2. Di sidebar kiri, klik **"Environment Variables"**

### Step 4: Tambah/Edit Variable

#### Jika Variable Belum Ada:

1. Klik tombol **"Add New"**
2. Isi form:
   - **Name:** `VITE_API_BASE_URL`
   - **Value:** `https://p2h-api-production.up.railway.app`
   - **Environments:** ✅ Centang semua (Production, Preview, Development)
3. Klik **"Save"**

#### Jika Variable Sudah Ada (tapi value salah):

1. Cari variable `VITE_API_BASE_URL`
2. Klik **ikon pensil** (Edit)
3. Update **Value** menjadi: `https://p2h-api-production.up.railway.app`
4. Klik **"Save"**

### Step 5: Redeploy

Setelah save environment variable, Vercel akan minta redeploy.

**Opsi A - Auto Redeploy (Recommended):**

Vercel akan otomatis redeploy karena Anda sudah push ke GitHub tadi.

1. Klik tab **"Deployments"**
2. Lihat deployment terbaru (paling atas)
3. Tunggu sampai status **"Ready"** (biasanya 1-2 menit)

**Opsi B - Manual Redeploy:**

1. Klik tab **"Deployments"**
2. Klik deployment terakhir yang sukses
3. Klik tombol **"⋯"** (3 dots)
4. Pilih **"Redeploy"**
5. Confirm

---

## ✅ Verifikasi Setelah Redeploy

### 1. Tunggu Deployment Selesai

Di tab **Deployments**, tunggu sampai status **"Ready"** dengan ✅ hijau.

### 2. Test Frontend

1. Buka **https://p2h-web.vercel.app** di browser
2. Tekan **Ctrl+Shift+R** (hard refresh untuk clear cache)
3. Buka **DevTools** (F12)
4. Klik tab **"Network"**
5. Login atau refresh page

### 3. Cek Request URL

Di Network tab, klik salah satu request API (misalnya `login` atau `reports`).

**✅ BENAR - Jika lihat:**

```
Request URL: https://p2h-api-production.up.railway.app/auth/login
Status: 200 OK (atau 401 jika belum login)
```

**❌ MASIH SALAH - Jika lihat:**

```
Request URL: https://p2h-web-production.up.railway.app/...
```

Jika masih salah, kemungkinan:

- Environment variable belum save dengan benar
- Belum redeploy
- Browser cache belum clear (coba Incognito mode)

---

## 🔧 Troubleshooting

### Environment Variable Tidak Muncul

- Pastikan Anda di project yang benar
- Refresh halaman Vercel dashboard
- Coba logout/login Vercel

### Redeploy Tidak Otomatis

- Buat commit dummy dan push:
  ```bash
  git commit --allow-empty -m "Trigger Vercel redeploy"
  git push
  ```

### Masih Memanggil URL Lama

- Clear browser cache atau pakai **Incognito mode**
- Pastikan environment variable **Value** benar (tanpa typo)
- Pastikan environment variable untuk **Production** environment

### CORS Error Masih Ada

Setelah URL benar, jika masih ada CORS error:

1. Buka Railway **backend** project
2. Tab **Variables**
3. Edit `CORS_ORIGINS`:
   ```json
   ["http://localhost:5173", "https://p2h-web.vercel.app"]
   ```
4. Save → backend akan auto-redeploy

---

## 📸 Screenshot Checklist

Saat di Vercel Settings → Environment Variables, pastikan:

- ✅ Variable name: `VITE_API_BASE_URL`
- ✅ Value: `https://p2h-api-production.up.railway.app`
- ✅ Environment: Production ✓
- ✅ Status: Saved (ada checkmark hijau)

---

## ⏱️ Timeline

1. **Update env var:** 1 menit
2. **Redeploy:** 1-2 menit (otomatis)
3. **Test:** 1 menit

**Total:** ~5 menit

---

## 🆘 Jika Masih Stuck

Coba set sementara CORS backend ke `*` untuk testing:

Di Railway backend Variables:

```
CORS_ORIGINS=*
```

Jika dengan `*` masih error, berarti masalah bukan di CORS, tapi di URL atau backend down.
