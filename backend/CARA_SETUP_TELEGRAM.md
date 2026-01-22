# 🚀 CARA MENGAKTIFKAN NOTIFIKASI TELEGRAM

## ⚡ Quick Start (3 Menit Setup!)

### 1️⃣ Buat Bot Telegram

1. Buka Telegram, cari **@BotFather**
2. Ketik: `/newbot`
3. Beri nama bot (contoh: `P2H IMM Alert Bot`)
4. Beri username (contoh: `p2h_imm_alert_bot`)
5. **Simpan TOKEN** yang diberikan!

### 2️⃣ Dapatkan Chat ID Anda

1. Cari **@userinfobot** di Telegram
2. Klik `/start`
3. **Simpan ID** yang muncul (angka seperti `123456789`)

### 3️⃣ Konfigurasi Backend

File yang sudah Anda buka sekarang (`.env`) sudah ada konfigurasinya:

```env
TELEGRAM_BOT_TOKEN=8452421112:AAFvXNHSyMDp6CuDN-06OHEAe3wTqehkm8U
TELEGRAM_CHAT_ID=8169592330
```

**Ganti dengan kredensial Anda:**
```env
TELEGRAM_BOT_TOKEN=<token_dari_botfather>
TELEGRAM_CHAT_ID=<id_dari_userinfobot>
```

### 4️⃣ Start Bot Anda

1. Cari bot Anda di Telegram (sesuai username tadi)
2. Klik **START**
3. Done! Bot siap menerima notifikasi

### 5️⃣ Test Koneksi

Buka terminal baru dan jalankan:

```powershell
# Masuk ke folder backend
cd D:\PT-IMM-P2H\backend

# Aktifkan virtual environment
.\.venv\Scripts\Activate.ps1

# Jalankan test bot
python test_telegram_bot.py
```

Jika berhasil, Anda akan menerima pesan test di Telegram! 🎉

---

## 📱 Kapan Notifikasi Akan Terkirim?

### ✅ Otomatis Terkirim:

1. **Saat user submit P2H dengan status WARNING**
   - Langsung kirim ke Telegram
   - Mencatat ke database
   
2. **Saat user submit P2H dengan status ABNORMAL**
   - Langsung kirim ke Telegram
   - Mencatat ke database

3. **Status NORMAL**: Tidak ada notifikasi (normal saja)

---

## 🔍 Cara Kerja Sistem

```
User Submit P2H → Backend Analisa Status → Jika WARNING/ABNORMAL → Kirim ke Telegram
                                         → Jika NORMAL → Skip notifikasi
```

**Tidak perlu setting apapun lagi!** Sistem sudah otomatis.

---

## 📊 Monitoring Notifikasi

Cek notifikasi yang terkirim di database:

```sql
SELECT 
    notification_type,
    is_sent,
    sent_at,
    created_at
FROM telegram_notifications
ORDER BY created_at DESC;
```

---

## ❓ Troubleshooting

### Bot tidak kirim pesan?

1. ✅ Pastikan sudah klik **START** pada bot
2. ✅ Cek `TELEGRAM_BOT_TOKEN` dan `TELEGRAM_CHAT_ID` di `.env`
3. ✅ Restart backend setelah ubah `.env`:
   ```powershell
   # Ctrl+C untuk stop backend
   # Kemudian jalankan lagi:
   uvicorn app.main:app --reload --port 8000
   ```

### Error "Unauthorized"?

- Token bot salah → Generate ulang dari @BotFather

### Error "Chat not found"?

- Chat ID salah → Cek ulang dari @userinfobot
- Belum /start bot → Start dulu bot di Telegram

---

## 🎯 Apa yang Sudah Ready?

✅ Model database `telegram_notifications`  
✅ Service untuk kirim pesan  
✅ Auto-trigger saat P2H WARNING/ABNORMAL  
✅ Format pesan yang informatif  
✅ Error handling dan logging  
✅ Script testing lengkap  

**Tinggal konfigurasi token dan chat ID saja!**

---

## 📖 Dokumentasi Lengkap

Baca file [TELEGRAM_INTEGRATION.md](TELEGRAM_INTEGRATION.md) untuk:
- Format pesan detail
- Troubleshooting advanced
- Enhancement ideas
- Database schema

---

**Sistem siap pakai! 🚀**
