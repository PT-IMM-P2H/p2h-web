# Panduan Singkat: Mengatasi Masalah Telegram Tidak Berfungsi

## Masalah

User baru sudah scan bot telegram dan kirim `/start`, tapi notifikasi tidak terkirim.

## Penyebab

Sistem sebelumnya menggunakan **satu TELEGRAM_CHAT_ID global** untuk semua notifikasi, bukan chat_id personal setiap user.

## Solusi Lengkap

Sudah diimplementasikan sistem baru dengan fitur:

### ✅ 1. Model User Ditambahkan Field Telegram
- `telegram_chat_id` - Chat ID personal user
- `telegram_username` - Username telegram user
- `telegram_linked_at` - Waktu linking

### ✅ 2. Migration Database
File: `alembic/versions/2026_02_05_1526-a553b45fe239_add_telegram_chat_id_to_users.py`

**Jalankan migration:**
```bash
cd backend
python -m alembic upgrade head
```

### ✅ 3. Telegram Bot dengan Command Handler
File: `app/services/telegram_bot.py`

Bot sekarang support command:
- `/start NOMOR_HP` - Link akun telegram dengan P2H
- `/status` - Cek status linking
- `/help` - Bantuan

### ✅ 4. TelegramService Updated
File: `app/services/telegram_service.py`

Sekarang mengirim notifikasi ke:
- **Chat pribadi user** (jika sudah link telegram)
- **Grup default** (fallback jika belum link)

### ✅ 5. API Endpoints
File: `app/routers/users.py`

Endpoint baru:
- `POST /api/users/telegram/link` - Link telegram
- `GET /api/users/me/telegram/status` - Cek status
- `DELETE /api/users/me/telegram/unlink` - Unlink telegram

### ✅ 6. Dokumentasi Lengkap
File: `docs/TELEGRAM_PERSONAL_INTEGRATION.md`

## Langkah Deploy

### 1. Jalankan Migration
```bash
cd backend
python -m alembic upgrade head
```

### 2. Start Telegram Bot
**Development:**
```bash
cd backend
python -m app.services.telegram_bot
```

**Production (systemd):**
```bash
# Buat file /etc/systemd/system/p2h-telegram-bot.service
sudo systemctl enable p2h-telegram-bot
sudo systemctl start p2h-telegram-bot
sudo systemctl status p2h-telegram-bot
```

### 3. Minta User Link Telegram
Setiap user harus:
1. Buka bot telegram
2. Kirim: `/start NOMOR_TELEPON_MEREKA`
3. Bot akan confirm jika berhasil

### 4. Verify
```bash
# Cek user yang sudah link
python -c "
from app.database import SessionLocal
from app.models.user import User
db = SessionLocal()
linked = db.query(User).filter(User.telegram_chat_id.isnot(None)).count()
total = db.query(User).count()
print(f'Linked: {linked}/{total} users')
"
```

## Test Flow

### Test 1: Link Telegram
1. Buka telegram bot
2. Kirim: `/start 081234567890`
3. Expect: Bot balas "✅ Berhasil Terhubung!"

### Test 2: Submit P2H Warning/Abnormal
1. User submit P2H dengan status WARNING
2. Expect: Notifikasi masuk ke chat pribadi user
3. Jika user belum link: Notifikasi ke grup default

### Test 3: Cek Status via API
```bash
curl -X GET http://localhost:8000/api/users/me/telegram/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Troubleshooting

### Bot tidak merespon
```bash
# Cek bot running
ps aux | grep telegram_bot

# Restart bot
sudo systemctl restart p2h-telegram-bot

# Cek logs
journalctl -u p2h-telegram-bot -f
```

### User tidak bisa link
```sql
-- Cek nomor telepon di database
SELECT id, full_name, phone_number, telegram_chat_id 
FROM users 
WHERE phone_number = '081234567890';

-- Reset telegram link jika perlu
UPDATE users 
SET telegram_chat_id = NULL 
WHERE phone_number = '081234567890';
```

### Notifikasi tidak terkirim
1. Cek user sudah link: `GET /api/users/me/telegram/status`
2. Cek bot token: `python check_telegram_config.py`
3. Cek network: `ping api.telegram.org`

## Catatan Penting

⚠️ **Bot harus running sebagai background service** untuk menerima command dari user.

⚠️ **Setiap user harus link telegram mereka sendiri** dengan command `/start`.

⚠️ **Fallback ke grup masih aktif** untuk user yang belum link telegram.

## Quick Reference

**Command user di telegram:**
```
/start 081234567890  → Link akun
/status              → Cek status
/help                → Bantuan
```

**Migration:**
```bash
python -m alembic upgrade head
```

**Start bot:**
```bash
python -m app.services.telegram_bot
```

**Check linked users:**
```sql
SELECT COUNT(*) FROM users WHERE telegram_chat_id IS NOT NULL;
```

Untuk detail lengkap, baca: [TELEGRAM_PERSONAL_INTEGRATION.md](./TELEGRAM_PERSONAL_INTEGRATION.md)
