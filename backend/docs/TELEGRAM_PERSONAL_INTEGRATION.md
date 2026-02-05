# Telegram Notification - Personal Chat Integration

## Gambaran Umum

Sistem P2H sekarang mendukung **notifikasi Telegram personal** untuk setiap user. Setiap user dapat menghubungkan akun Telegram mereka sendiri dan menerima notifikasi P2H langsung di chat pribadi mereka.

## Cara Kerja

### 1. User Link Telegram Account

**User harus menghubungkan Telegram mereka dengan mengikuti langkah berikut:**

1. Buka Telegram dan cari bot P2H: `@YourBotName` (sesuai dengan bot yang sudah dibuat)
2. Kirim command: `/start NOMOR_TELEPON`
   - Contoh: `/start 081234567890`
   - Gunakan nomor telepon yang sama dengan akun P2H Anda
3. Bot akan membalas jika berhasil atau error jika nomor tidak ditemukan

**Contoh Interaksi:**

```
User: /start 081234567890
Bot: ✅ Berhasil Terhubung!

     Akun Telegram Anda telah terhubung dengan:
     • Nama: John Doe
     • Nomor: 081234567890
     • Role: user
     
     🔔 Anda akan menerima notifikasi P2H di chat ini.
```

### 2. Bot Commands

Bot mendukung command berikut:

- **`/start NOMOR_HP`** - Hubungkan akun Telegram dengan akun P2H
- **`/status`** - Cek status koneksi akun
- **`/help`** - Tampilkan bantuan

### 3. Notifikasi Otomatis

Setelah terhubung, user akan menerima notifikasi di chat Telegram pribadi mereka ketika:

- **P2H Abnormal** - Unit dalam status ABNORMAL (STOP OPERASI)
- **P2H Warning** - Unit dalam status WARNING (PERLU PERBAIKAN)

**Catatan:** 
- Jika user belum link telegram, notifikasi akan dikirim ke grup default (jika `TELEGRAM_CHAT_ID` diset)
- Notifikasi dokumen expiry (STNK/KIR) masih dikirim ke grup admin

## Setup Bot Telegram

### 1. Buat Bot dengan BotFather

1. Buka Telegram dan cari: `@BotFather`
2. Kirim command: `/newbot`
3. Ikuti instruksi untuk set nama bot
4. Simpan **Bot Token** yang diberikan

### 2. Set Environment Variables

Tambahkan ke `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_group_chat_id_for_admin_notifications  # Optional: untuk admin group
```

### 3. Jalankan Migration

```bash
cd backend
python -m alembic upgrade head
```

Migration akan menambahkan field:
- `telegram_chat_id` (String, unique)
- `telegram_username` (String, optional)
- `telegram_linked_at` (DateTime)

### 4. Jalankan Telegram Bot

Bot perlu berjalan sebagai **background process** terpisah dari FastAPI:

```bash
cd backend
python -m app.services.telegram_bot
```

**Untuk Production (dengan systemd/supervisor):**

Create service file `/etc/systemd/system/p2h-telegram-bot.service`:

```ini
[Unit]
Description=P2H Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python -m app.services.telegram_bot
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable dan start:
```bash
sudo systemctl enable p2h-telegram-bot
sudo systemctl start p2h-telegram-bot
sudo systemctl status p2h-telegram-bot
```

## API Endpoints

### Link Telegram (Internal - Called by Bot)

```http
POST /api/users/telegram/link
Content-Type: application/json

{
  "phone_number": "081234567890",
  "telegram_chat_id": "123456789",
  "telegram_username": "johndoe"
}
```

### Get Telegram Status (User)

```http
GET /api/users/me/telegram/status
Authorization: Bearer {token}
```

Response:
```json
{
  "success": true,
  "message": "Status telegram berhasil diambil",
  "payload": {
    "is_linked": true,
    "telegram_chat_id": "123456789",
    "telegram_username": "johndoe",
    "telegram_linked_at": "2026-02-05T15:30:00"
  }
}
```

### Unlink Telegram (User)

```http
DELETE /api/users/me/telegram/unlink
Authorization: Bearer {token}
```

## Troubleshooting

### Bot Tidak Merespon

1. **Pastikan bot running:**
   ```bash
   systemctl status p2h-telegram-bot  # Untuk production
   # Atau jalankan manual untuk test:
   python -m app.services.telegram_bot
   ```

2. **Cek token bot:**
   ```bash
   python check_telegram_config.py
   ```

3. **Cek logs:**
   ```bash
   journalctl -u p2h-telegram-bot -f  # Production
   ```

### User Tidak Dapat Link

1. **Nomor tidak ditemukan:**
   - Pastikan nomor telepon exact match dengan database
   - Cek di database: `SELECT * FROM users WHERE phone_number = '081234567890'`

2. **Chat ID sudah digunakan:**
   - Unlink dari user lama terlebih dahulu
   - Atau hubungi admin untuk reset

3. **Bot tidak menerima command:**
   - Pastikan bot sudah di-start dengan `/start` di chat
   - Restart bot process

### Notifikasi Tidak Terkirim

1. **User belum link telegram:**
   - Minta user jalankan `/start NOMOR_HP` di bot
   - Cek status: `GET /api/users/me/telegram/status`

2. **Bot token invalid:**
   - Regenerate token di BotFather
   - Update `TELEGRAM_BOT_TOKEN` di environment

3. **Network issues:**
   - Pastikan server bisa akses `api.telegram.org`
   - Cek firewall/proxy settings

## Database Schema

### Tabel: users

```sql
ALTER TABLE users ADD COLUMN telegram_chat_id VARCHAR(100) UNIQUE;
ALTER TABLE users ADD COLUMN telegram_username VARCHAR(100);
ALTER TABLE users ADD COLUMN telegram_linked_at TIMESTAMP;
```

### Query Useful

**Cek semua user yang sudah link telegram:**
```sql
SELECT full_name, phone_number, telegram_username, telegram_linked_at
FROM users
WHERE telegram_chat_id IS NOT NULL
ORDER BY telegram_linked_at DESC;
```

**Unlink telegram untuk user tertentu:**
```sql
UPDATE users
SET telegram_chat_id = NULL, 
    telegram_username = NULL, 
    telegram_linked_at = NULL
WHERE phone_number = '081234567890';
```

## Alur Notifikasi

### P2H Abnormal/Warning

1. User submit P2H dengan status ABNORMAL/WARNING
2. System create record di `telegram_notifications`
3. System cek `report.user.telegram_chat_id`
4. Jika ada chat_id:
   - Kirim notifikasi ke chat pribadi user
5. Jika belum link:
   - Kirim ke grup default (fallback)
   - Log warning: "User belum link telegram"

### Dokumen Expiry (STNK/KIR)

1. Scheduler job cek expiry documents
2. System create notification di database
3. Kirim ke grup admin (menggunakan `TELEGRAM_CHAT_ID` dari config)

## Best Practices

1. **Setiap user harus link telegram sendiri** untuk menerima notifikasi personal
2. **Bot harus selalu running** sebagai background service
3. **Monitor bot health** dengan systemd/supervisor
4. **Set TELEGRAM_CHAT_ID** untuk grup admin sebagai fallback
5. **Test bot** sebelum deploy production:
   ```bash
   python -m app.services.telegram_bot
   ```

## Migration dari Grup ke Personal Chat

Jika sebelumnya menggunakan satu grup untuk semua notifikasi:

1. **Jalankan migration** untuk menambah field `telegram_chat_id`
2. **Start telegram bot** sebagai background service
3. **Minta semua user untuk link** telegram mereka:
   - Kirim announcement: "Scan bot telegram dan kirim /start NOMOR_HP"
4. **Monitor adoption rate**:
   ```sql
   SELECT 
     COUNT(*) as total_users,
     COUNT(telegram_chat_id) as linked_users,
     ROUND(COUNT(telegram_chat_id) * 100.0 / COUNT(*), 2) as percentage
   FROM users;
   ```
5. **Grup tetap aktif** sebagai fallback untuk user yang belum link

## Support

Jika ada masalah:
1. Cek logs bot: `journalctl -u p2h-telegram-bot -f`
2. Test koneksi: `python test_telegram_connection.py`
3. Cek database: Query user dan notification tables
4. Contact backend developer untuk troubleshooting lebih lanjut
