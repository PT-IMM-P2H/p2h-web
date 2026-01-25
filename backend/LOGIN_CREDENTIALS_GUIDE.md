# 🔐 Login Credentials & Testing Guide

## 📋 Default User Accounts

After running `seed_users`, these accounts will be available:

### 1. Superadmin Account

```
Email/Username: yunnifa@imm.co.id
Phone Number:   085754538366
Password:       yunnifa12062003
Role:           superadmin
```

**Password Formula:** `namadepan` + `DDMMYYYY`

- Nama: **Yunnifa** Nur Lailli
- Tanggal Lahir: **12-06-2003**
- Password: `yunnifa` + `12062003` = **yunnifa12062003**

---

### 2. Regular User Account

```
Email/Username: budi@imm.co.id
Phone Number:   081234567890
Password:       budi15051990
Role:           user
```

**Password Formula:** `namadepan` + `DDMMYYYY`

- Nama: **Budi** Santoso
- Tanggal Lahir: **15-05-1990**
- Password: `budi` + `15051990` = **budi15051990**

---

## 🧪 How to Test Login

### Option 1: Login with Email

```json
{
  "username": "yunnifa@imm.co.id",
  "password": "yunnifa12062003"
}
```

### Option 2: Login with Phone Number

```json
{
  "username": "085754538366",
  "password": "yunnifa12062003"
}
```

---

## 🔍 Debugging Login Issues

### Check Railway Logs

After attempting login, check Railway logs for these messages:

#### ✅ Successful Login:

```
🔐 Login attempt with username: yunnifa@imm.co.id
✅ User found: Yunnifa Nur Lailli (ID: ...)
✅ Password verified for user: Yunnifa Nur Lailli
✅ Login successful: Yunnifa Nur Lailli (superadmin)
```

#### ❌ User Not Found:

```
🔐 Login attempt with username: wrong@email.com
❌ User not found: wrong@email.com
```

**Solution:** Check if user exists in database. Run seed_users again.

#### ❌ Wrong Password:

```
🔐 Login attempt with username: yunnifa@imm.co.id
✅ User found: Yunnifa Nur Lailli (ID: ...)
❌ Password mismatch for user: Yunnifa Nur Lailli
```

**Solution:** Verify password formula. Check if password was hashed correctly during seeding.

#### ❌ User Inactive:

```
🔐 Login attempt with username: yunnifa@imm.co.id
✅ User found: Yunnifa Nur Lailli (ID: ...)
✅ Password verified for user: Yunnifa Nur Lailli
❌ User inactive: Yunnifa Nur Lailli
```

**Solution:** User exists but `is_active = False`. Update user in database.

---

## 🛠️ Manual Testing via Swagger

1. Go to: `https://p2h-web-production.up.railway.app/docs`
2. Find `POST /auth/login`
3. Click "Try it out"
4. Fill in:
   ```
   username: yunnifa@imm.co.id
   password: yunnifa12062003
   ```
5. Click "Execute"
6. Check response

---

## 🔧 Verify Seed Users Ran Successfully

Check Railway deployment logs for:

```
✅ Akun superadmin baru berhasil dibuat: Yunnifa Nur Lailli
==================================================
User     : Yunnifa Nur Lailli
Role     : superadmin
Phone    : 085754538366
Password : yunnifa12062003
==================================================

✅ Akun user baru berhasil dibuat: Budi Santoso
==================================================
User     : Budi Santoso
Role     : user
Phone    : 081234567890
Password : budi15051990
==================================================
```

If you **DON'T** see these messages, the seed script didn't run or failed.

---

## 🐛 Common Issues

### Issue 1: Seed Script Didn't Run

**Symptom:** No seed messages in Railway logs  
**Cause:** `startCommand` in railway.json not updated  
**Solution:** Verify railway.json has:

```json
"startCommand": "python -m app.seeds.seed_users && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### Issue 2: Database Connection Error During Seed

**Symptom:** Error in logs during seed_users  
**Cause:** Database not ready yet  
**Solution:** Seed script should wait for DB. Check `seed_users.py` has proper error handling.

### Issue 3: Password Hash Mismatch

**Symptom:** "Password mismatch" in logs  
**Cause:** Password hashed differently during seed vs login  
**Solution:** Both use same `hash_password()` function. Check bcrypt version.

### Issue 4: CORS Error (Again)

**Symptom:** Request blocked before reaching login endpoint  
**Cause:** CORS not configured properly  
**Solution:** Verify `ENVIRONMENT=production` and `CORS_ORIGINS` in Railway

---

## 📊 Expected Login Flow

1. **Frontend sends:**

   ```
   POST /auth/login
   Content-Type: application/x-www-form-urlencoded

   username=yunnifa@imm.co.id&password=yunnifa12062003
   ```

2. **Backend logs:**

   ```
   🔐 Login attempt with username: yunnifa@imm.co.id
   ✅ User found: Yunnifa Nur Lailli (ID: ...)
   ✅ Password verified for user: Yunnifa Nur Lailli
   ✅ Login successful: Yunnifa Nur Lailli (superadmin)
   ```

3. **Backend responds:**

   ```json
   {
     "success": true,
     "message": "Login Berhasil",
     "payload": {
       "user": { ... },
       "access_token": "eyJ...",
       "token_type": "bearer"
     }
   }
   ```

4. **Cookie set:**
   ```
   Set-Cookie: access_token=eyJ...; HttpOnly; Secure; SameSite=Lax
   ```

---

## 🎯 Next Steps

1. **Push code changes** (auth_service.py with logging)
2. **Wait for Railway deploy**
3. **Check logs** for seed messages
4. **Try login** with credentials above
5. **Check logs** for authentication flow
6. **Report back** what you see in logs!

---

**Last Updated:** 2026-01-25
