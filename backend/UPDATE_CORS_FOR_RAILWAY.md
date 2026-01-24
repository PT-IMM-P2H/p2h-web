# Update CORS Backend untuk Railway Frontend

Setelah deploy frontend ke Railway dan mendapat domain, update CORS di backend:

## Di Railway Backend Dashboard

1. Buka project **backend** di Railway
2. Klik tab **"Variables"**
3. Edit variable **`CORS_ORIGINS`**
4. Update dengan format JSON array:

```json
[
  "http://localhost:5173",
  "https://p2h-web.vercel.app",
  "https://YOUR-FRONTEND-DOMAIN.railway.app"
]
```

**Ganti `YOUR-FRONTEND-DOMAIN.railway.app` dengan domain Railway frontend yang sebenarnya.**

## Format yang Benar

✅ **BENAR:**

```json
[
  "http://localhost:5173",
  "https://p2h-web.vercel.app",
  "https://p2h-frontend-production.up.railway.app"
]
```

❌ **SALAH:**

```
http://localhost:5173, https://p2h-web.vercel.app
```

❌ **SALAH:**

```json
["http://localhost:5173", "https://p2h-web.vercel.app"]
```

## Setelah Update

1. Klik **"Save"**
2. Backend akan **auto-redeploy** (tunggu ~1-2 menit)
3. Test frontend lagi - CORS error seharusnya hilang

## Verifikasi

Buka frontend → DevTools (F12) → Network tab → klik request ke backend → lihat Response Headers:

Harus ada:

```
Access-Control-Allow-Origin: https://your-frontend.railway.app
```
