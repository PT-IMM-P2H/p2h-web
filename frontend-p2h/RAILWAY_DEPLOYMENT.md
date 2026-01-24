# 🚀 Cara Deploy Frontend ke Railway

## Ringkasan Singkat

Railway akan otomatis build dan deploy frontend Anda. Yang perlu dilakukan:

1. **Push code ke GitHub** (termasuk `railway.json` dan `nixpacks.toml` yang sudah dibuat)
2. **Buat project di Railway** dan connect ke repo
3. **Set Root Directory** ke `frontend-p2h`
4. **Update CORS di backend** untuk allow domain Railway frontend

---

## 📝 Langkah Detail

### 1. Push ke GitHub

```bash
cd e:\Magang\Github-P2H-web\p2h-web\frontend-p2h
git add railway.json nixpacks.toml index.html RAILWAY_DEPLOYMENT.md
git commit -m "Add Railway deployment configuration"
git push
```

### 2. Setup di Railway

1. Login ke **https://railway.app**
2. Klik **"New Project"** → **"Deploy from GitHub repo"**
3. Pilih repository **`p2h-web`**
4. Railway akan auto-detect dan mulai deploy

### 3. Configure Root Directory

Karena frontend ada di subfolder:

1. Klik project yang baru dibuat
2. Klik tab **"Settings"**
3. Scroll ke **"Root Directory"**
4. Isi: `frontend-p2h`
5. Klik **"Save"**

Railway akan auto-redeploy dengan konfigurasi baru.

### 4. Dapatkan Domain

Setelah deploy selesai:

1. Klik tab **"Settings"**
2. Scroll ke **"Domains"**
3. Klik **"Generate Domain"**
4. Copy domain yang didapat (contoh: `p2h-frontend-production.up.railway.app`)

---

## ⚠️ PENTING: Update CORS di Backend

Setelah dapat domain Railway frontend, **WAJIB** update CORS di backend Railway:

### Di Railway Backend Dashboard:

1. Buka **backend project** di Railway
2. Klik tab **"Variables"**
3. Cari variable **`CORS_ORIGINS`**
4. Update valuenya menjadi (ganti dengan domain Railway frontend Anda):

```json
[
  "http://localhost:5173",
  "https://p2h-web.vercel.app",
  "https://p2h-frontend-production.up.railway.app"
]
```

**Format:** JSON array dengan double quotes, tanpa spasi setelah koma.

5. Klik **"Save"**
6. Backend akan auto-redeploy dengan CORS baru

---

## ✅ Verifikasi

### Test Frontend

1. Buka domain Railway frontend di browser
2. Buka **DevTools** (F12) → **Console**
3. Login ke aplikasi
4. Pastikan **TIDAK ADA** error CORS atau CSP

### Cek CORS Headers

Di DevTools → **Network** tab:

- Klik request ke backend
- Lihat **Response Headers**
- Pastikan ada: `Access-Control-Allow-Origin: https://your-frontend.railway.app`

---

## 🔧 Troubleshooting

### ❌ Build Failed

**Cek logs di Railway:**

- Tab "Deployments" → klik deployment yang failed → lihat logs

**Common issues:**

- Missing dependencies → pastikan `package.json` lengkap
- Build script error → test `npm run build` di local dulu

### ❌ CORS Error Masih Muncul

**Solusi:**

1. Pastikan domain Railway frontend sudah ditambahkan di `CORS_ORIGINS` backend
2. Format harus JSON array dengan double quotes
3. Restart backend setelah update environment variable
4. Clear browser cache dan hard refresh (Ctrl+Shift+R)

### ❌ CSP Error

**Solusi:**

- Production build **tidak perlu** `unsafe-eval`
- `index.html` sudah diupdate untuk remove `unsafe-eval`
- Jika masih error, cek browser console untuk detail

### ❌ Blank Page / 404 Error

**Solusi:**

- Pastikan `Root Directory` di Railway settings sudah set ke `frontend-p2h`
- Cek logs untuk error saat build
- Pastikan `dist` folder ter-generate dengan benar

---

## 🔄 Update Deployment

Setiap kali push ke GitHub branch yang connected, Railway akan **auto-deploy** ulang.

```bash
# Make changes
git add .
git commit -m "Update feature X"
git push

# Railway akan otomatis detect dan deploy
```

---

## 📊 Monitoring

Di Railway dashboard:

- **Deployments** tab: lihat history deployment
- **Metrics** tab: lihat usage CPU, memory, bandwidth
- **Logs** tab: lihat real-time logs aplikasi

---

## 💡 Tips

1. **Environment Variables**: Jika perlu API URL dinamis, tambahkan di Railway Variables:

   ```
   VITE_API_URL=https://p2h-web-production.up.railway.app
   ```

2. **Custom Domain**: Bisa tambahkan custom domain di Settings → Domains

3. **Preview Deployments**: Setiap PR bisa auto-deploy ke preview URL

---

## 📚 Resources

- [Railway Docs](https://docs.railway.app)
- [Nixpacks Docs](https://nixpacks.com/docs)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)
