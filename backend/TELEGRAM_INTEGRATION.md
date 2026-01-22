# 🤖 Integrasi Telegram Bot untuk Auto Notifikasi

## 📋 Daftar Isi
1. [Overview](#overview)
2. [Kapan Notifikasi Dikirim](#kapan-notifikasi-dikirim)
3. [Setup Bot Telegram](#setup-bot-telegram)
4. [Testing Koneksi](#testing-koneksi)
5. [Format Pesan](#format-pesan)
6. [Troubleshooting](#troubleshooting)

---

## Overview

Sistem P2H telah dilengkapi dengan **Auto Notification ke Telegram Bot** yang akan mengirimkan alert secara otomatis ketika:

✅ **P2H Status ABNORMAL** (Unit tidak boleh operasi)  
✅ **P2H Status WARNING** (Unit perlu perbaikan)  
✅ **STNK/KIR akan expired** (7 hari sebelumnya)  
✅ **STNK/KIR sudah expired** (notifikasi urgent)

---

## Kapan Notifikasi Dikirim

### 1️⃣ Saat Submit P2H dengan Status Bermasalah

Ketika user mengisi form P2H dan hasilnya:
- **WARNING**: Langsung kirim notifikasi ke Telegram
- **ABNORMAL**: Langsung kirim notifikasi ke Telegram  
- **NORMAL**: Tidak ada notifikasi

**Lokasi Kode:**
- File: `backend/app/services/p2h_service.py`
- Fungsi: `submit_p2h()` baris 176-182
- Trigger: Otomatis saat API POST `/api/p2h/reports` dipanggil

```python
# Auto-trigger di dalam submit_p2h()
if overall_status in [InspectionStatus.ABNORMAL, InspectionStatus.WARNING]:
    try:
        await telegram_service.send_p2h_notification(
            db, vehicle, report, overall_status
        )
    except Exception as e:
        logger.error(f"Telegram alert failed: {str(e)}")
```

### 2️⃣ Scheduler Harian untuk Expired Dokumen (Coming Soon)

Akan ada scheduler job yang berjalan setiap hari untuk mengecek:
- STNK yang akan expired dalam 7, 3, atau 1 hari
- KIR yang akan expired dalam 7, 3, atau 1 hari
- Dokumen yang sudah expired

**Status**: Belum diimplementasikan (perlu setup APScheduler)

---

## Setup Bot Telegram

### Langkah 1: Buat Bot Telegram Baru

1. Buka Telegram dan cari **@BotFather**
2. Ketik `/newbot`
3. Ikuti instruksi untuk memberi nama bot
4. Simpan **Token** yang diberikan (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Langkah 2: Dapatkan Chat ID

**Cara 1: Menggunakan @userinfobot**
1. Cari bot **@userinfobot** di Telegram
2. Klik `/start`
3. Bot akan menampilkan **ID** Anda (angka seperti `123456789`)

**Cara 2: Menggunakan API (jika untuk grup)**
1. Tambahkan bot ke grup Telegram
2. Kirim pesan di grup
3. Buka browser dan akses:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Cari `"chat":{"id":-1001234567890}` di response JSON

### Langkah 3: Konfigurasi di Backend

Edit file `backend/.env`:

```env
# =========================================================================
# TELEGRAM NOTIFICATION
# =========================================================================
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
```

**PENTING:**
- `TELEGRAM_BOT_TOKEN`: Token dari @BotFather
- `TELEGRAM_CHAT_ID`: ID personal atau ID grup (dengan minus untuk grup)

### Langkah 4: Start Bot

Sebelum bot bisa mengirim pesan, Anda harus:
1. Cari bot Anda di Telegram (sesuai username yang dibuat)
2. Klik **START** atau ketik `/start`
3. Bot sekarang bisa mengirim pesan ke Anda

---

## Testing Koneksi

### Quick Test

Jalankan script test yang sudah disediakan:

```bash
# Pastikan virtual environment aktif
cd backend
.\.venv\Scripts\Activate.ps1

# Install dependency jika belum
pip install httpx python-dotenv

# Jalankan test
python test_telegram_bot.py
```

**Output yang diharapkan:**
```
==================================================
   TELEGRAM BOT CONNECTION TEST
   PT. IMM - P2H System
==================================================
🔍 Testing Telegram Bot Connection...
   Bot Token: 8452421112:AAFvXNHS...
   Chat ID: 8169592330
✅ Bot Connected Successfully!
   Bot Name: @your_bot_name
   Bot First Name: Your Bot

📤 Sending Test Message...
✅ Test message sent successfully!
   Silakan cek aplikasi Telegram Anda

==================================================
📋 Kirim demo notifikasi? (y/n): y

📤 Sending P2H WARNING Demo...
✅ P2H WARNING demo sent!

📤 Sending P2H ABNORMAL Demo...
✅ P2H ABNORMAL demo sent!

📤 Sending EXPIRY Alert Demo...
✅ EXPIRY alert demo sent!

==================================================
✅ Semua demo notifikasi berhasil dikirim!
   Silakan cek aplikasi Telegram Anda
==================================================
```

---

## Format Pesan

### 1. P2H WARNING

```
⚠️ P2H ALERT: WARNING (PERLU PERBAIKAN)
━━━━━━━━━━━━━━━━━━━━
Unit: DT-001
Tipe: Dump Truck
Merk/Plat: Hino / DA 1234 AB

📅 Detail Pemeriksaan:
Tanggal: 15 Jan 2026
Waktu: 08:30 WITA
Shift: 1
User: Budi Santoso

📝 Status Akhir: WARNING

⚠️ Tindakan: 
Harap segera melakukan pengecekan unit di workshop terdekat.
━━━━━━━━━━━━━━━━━━━━
Sistem P2H Digital PT. IMM
```

### 2. P2H ABNORMAL

```
❌ P2H ALERT: ABNORMAL (STOP OPERASI)
━━━━━━━━━━━━━━━━━━━━
Unit: EX-012
Tipe: Excavator
Merk/Plat: Komatsu / DA 5678 CD

📅 Detail Pemeriksaan:
Tanggal: 15 Jan 2026
Waktu: 14:15 WITA
Shift: 2
User: Ahmad Wijaya

📝 Status Akhir: ABNORMAL

⚠️ Tindakan: 
Harap segera melakukan pengecekan unit di workshop terdekat.
━━━━━━━━━━━━━━━━━━━━
Sistem P2H Digital PT. IMM
```

### 3. STNK/KIR Expired

```
🚨 EXPIRY ALERT: STNK
━━━━━━━━━━━━━━━━━━━━
Unit: TR-005
Plat Nomor: DA 9999 EF

📅 Detail Dokumen:
Jenis: STNK
Tanggal Expired: 20/01/2026
Sisa Waktu: 5 Hari Lagi

Status: 🔴 SANGAT SEGERA

💡 Info:
Harap segera memproses perpanjangan dokumen agar operasional tidak terganggu.
━━━━━━━━━━━━━━━━━━━━
Sistem Monitoring Asset PT. IMM
```

---

## Troubleshooting

### ❌ Bot tidak bisa kirim pesan

**Solusi:**
1. Pastikan Anda sudah klik **START** pada bot di Telegram
2. Cek apakah `TELEGRAM_CHAT_ID` sudah benar
3. Untuk grup, pastikan bot sudah ditambahkan dan diberi admin rights

### ❌ Error "Unauthorized"

**Penyebab:** Token bot salah

**Solusi:**
- Double check `TELEGRAM_BOT_TOKEN` di file `.env`
- Pastikan tidak ada spasi atau karakter tersembunyi
- Generate token baru dari @BotFather jika perlu

### ❌ Error "Chat not found"

**Penyebab:** Chat ID salah atau bot belum di-start

**Solusi:**
1. Pastikan Anda sudah `/start` bot
2. Verifikasi `TELEGRAM_CHAT_ID` menggunakan @userinfobot
3. Untuk grup, pastikan ID menggunakan tanda minus (contoh: `-1001234567890`)

### ❌ Pesan tidak sampai tapi tidak ada error

**Penyebab:** Bot di-block atau di-mute oleh user/grup

**Solusi:**
- Unblock bot di Telegram
- Pastikan notifikasi tidak dimute

---

## Database Logging

Setiap notifikasi yang dikirim (atau gagal) akan tercatat di tabel `telegram_notifications`:

```sql
SELECT 
    notification_type,
    is_sent,
    sent_at,
    error_message,
    message
FROM telegram_notifications
ORDER BY created_at DESC
LIMIT 10;
```

**Kolom Penting:**
- `is_sent`: `true` = berhasil, `false` = gagal
- `sent_at`: Timestamp kapan pesan berhasil terkirim
- `error_message`: Alasan kegagalan jika ada
- `message`: Isi pesan lengkap yang dikirim

---

## Next Steps (Enhancement)

### 🔄 Scheduler untuk Auto Check Expired

Implementasi scheduler harian untuk mengecek dokumen yang akan/sudah expired:

```python
# backend/app/scheduler/jobs.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', hour=7, minute=0)  # Setiap hari jam 7 pagi
async def check_document_expiry():
    """Cek STNK/KIR yang akan expired"""
    # Ambil semua kendaraan
    # Loop check STNK/KIR
    # Kirim notifikasi jika < 7 hari atau sudah expired
    pass
```

### 📊 Dashboard Admin untuk Monitoring Notifikasi

Tambahkan halaman admin untuk melihat:
- History notifikasi terkirim
- Grafik jumlah alert per hari
- Status pengiriman (berhasil/gagal)

### 🔔 Multiple Recipients

Support untuk kirim ke beberapa chat/grup sekaligus:

```env
TELEGRAM_CHAT_IDS=123456789,987654321,-1001234567890
```

---

## 📞 Support

Jika ada pertanyaan atau masalah:
1. Cek log di terminal backend
2. Cek tabel `telegram_notifications` di database
3. Jalankan `python test_telegram_bot.py` untuk diagnosa

**Sistem sudah siap digunakan!** 🚀
