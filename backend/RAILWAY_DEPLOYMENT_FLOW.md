# 🚀 Railway Deployment Flow - Updated

## 📋 New Deployment Sequence

Railway will now execute these commands in order on every deployment:

```bash
alembic upgrade head && python -m app.seeds.seed_users && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step-by-Step Breakdown:

#### 1️⃣ **Database Migration** (`alembic upgrade head`)

- Runs all pending Alembic migrations
- Creates/updates database schema (tables, columns, indexes)
- Ensures database structure is up-to-date
- **If fails:** Deployment stops, server won't start

#### 2️⃣ **Seed Users** (`python -m app.seeds.seed_users`)

- Creates/updates default user accounts
- Superadmin: yunnifa@imm.co.id
- User: budi@imm.co.id
- **If fails:** Deployment stops, server won't start

#### 3️⃣ **Start Server** (`uvicorn app.main:app --host 0.0.0.0 --port $PORT`)

- Starts FastAPI application
- Listens on Railway-provided port
- Starts scheduler for automated tasks
- **If fails:** Deployment marked as failed

---

## ✅ Benefits of This Approach

### 1. **Database Always Ready**

- Schema is migrated BEFORE seeding
- No more "table doesn't exist" errors
- Clean deployment every time

### 2. **Users Always Available**

- Default accounts created automatically
- No manual database seeding needed
- Can login immediately after deployment

### 3. **Fail-Fast Deployment**

- If migration fails → deployment stops
- If seeding fails → deployment stops
- Prevents broken deployments from going live

### 4. **No Duplicate Migrations**

- Migration removed from `main.py` lifespan
- Only runs once per deployment (in startCommand)
- Cleaner logs, faster startup

---

## 🔍 What to Look for in Railway Logs

### ✅ Successful Deployment:

```
[1/3] Running Alembic migrations...
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> abc123, create users table
✅ Migration completed

[2/3] Seeding users...
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

[3/3] Starting server...
====================================================================
                P2H SYSTEM PT. IMM BONTANG
====================================================================
🚀 Main API      : http://0.0.0.0:8080
📝 Swagger UI    : /docs
🌍 Environment   : production
🔧 Railway Mode  : Yes
====================================================================

✅ Scheduler started successfully
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### ❌ Migration Failed:

```
[1/3] Running Alembic migrations...
ERROR: relation "users" already exists
❌ Deployment stopped - migration failed
```

**Solution:** Check Alembic migration files, may need to resolve conflicts

---

### ❌ Seeding Failed:

```
[1/3] Running Alembic migrations...
✅ Migration completed

[2/3] Seeding users...
❌ Error: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "users_email_key"
❌ Deployment stopped - seeding failed
```

**Solution:** This is OK if users already exist. The seed script should handle this gracefully.

---

## 🔧 Files Modified

### 1. `railway.json`

```json
{
  "deploy": {
    "startCommand": "alembic upgrade head && python -m app.seeds.seed_users && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
  }
}
```

### 2. `Procfile`

```
web: alembic upgrade head && python -m app.seeds.seed_users && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3. `app/main.py`

```python
# Migration now handled in startCommand, not in lifespan
# run_alembic_migration()  # COMMENTED OUT
```

---

## 🎯 Testing the New Flow

### 1. Commit & Push Changes

```bash
git add railway.json Procfile app/main.py
git commit -m "feat: Run migrations and seed users before server start"
git push
```

### 2. Monitor Railway Deployment

- Go to Railway → Deployments tab
- Watch logs for the 3-step process
- Verify all steps complete successfully

### 3. Test Login

- Go to Vercel app
- Login with: `yunnifa@imm.co.id` / `yunnifa12062003`
- Should work immediately!

---

## 🐛 Troubleshooting

### Issue: Migration Hangs

**Symptom:** Deployment stuck at "Running Alembic migrations..."  
**Cause:** Database not accessible  
**Solution:** Check `DATABASE_URL` in Railway variables

### Issue: Seed Script Fails

**Symptom:** Error during user seeding  
**Cause:** Database schema mismatch or constraint violation  
**Solution:** Check if migration completed successfully first

### Issue: Server Won't Start

**Symptom:** Deployment fails after seeding  
**Cause:** Port binding or import errors  
**Solution:** Check Railway logs for Python errors

---

## 📊 Deployment Timeline

| Step              | Duration     | Can Fail? |
| ----------------- | ------------ | --------- |
| Build             | 30-60s       | Yes       |
| Alembic Migration | 5-10s        | Yes       |
| Seed Users        | 2-5s         | Yes       |
| Start Server      | 2-5s         | Yes       |
| **Total**         | **~1-2 min** | -         |

---

**Last Updated:** 2026-01-25
