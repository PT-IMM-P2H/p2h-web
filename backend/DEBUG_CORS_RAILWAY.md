# 🔍 Debug CORS Issues - Railway Logs Guide

## 🎯 Problem

CORS error: "No 'Access-Control-Allow-Origin' header is present"

This means the backend is **NOT sending CORS headers at all**, likely due to:

- ❌ Wrong `CORS_ORIGINS` format in Railway
- ❌ Backend failing to parse `CORS_ORIGINS`
- ❌ Backend crash during startup

---

## ✅ Solution: Check Railway Logs

### Step 1: Open Railway Logs

1. Go to https://railway.app/dashboard
2. Click on your **backend project** (`p2h-web-production`)
3. Click the **"Logs"** tab
4. Look at the **most recent deployment logs**

---

### Step 2: Look for CORS Messages

You should see **ONE** of these messages on startup:

#### ✅ **Success - Development Mode:**

```
🔓 CORS: Development mode - allowing all origins
```

#### ✅ **Success - Production with Wildcard:**

```
🔍 CORS: Raw CORS_ORIGINS value: ["http://localhost:5173","https://*.vercel.app"]
🔍 CORS: Parsed origins list: ['http://localhost:5173', 'https://*.vercel.app']
🔒 CORS: Production mode with wildcard - pattern: (http://localhost:5173)|(https://.*\.vercel\.app)
```

#### ✅ **Success - Production without Wildcard:**

```
🔍 CORS: Raw CORS_ORIGINS value: ["http://localhost:5173","https://p2h-web.vercel.app"]
🔍 CORS: Parsed origins list: ['http://localhost:5173', 'https://p2h-web.vercel.app']
🔒 CORS: Production mode - allowing origins: ['http://localhost:5173', 'https://p2h-web.vercel.app']
```

#### ❌ **Error - Config Failed (Fallback Active):**

```
❌ CORS configuration error: <error message>
⚠️ Falling back to allow all origins due to config error
```

---

### Step 3: Diagnose the Issue

#### Case 1: No CORS Messages at All

**Problem:** Backend crashed before reaching CORS setup

**Check for:**

- Database connection errors
- Alembic migration failures
- Import errors
- Missing environment variables

**Solution:** Fix the error shown in logs, then redeploy

---

#### Case 2: CORS Error Message Appears

**Problem:** `CORS_ORIGINS` format is wrong

**Common Errors:**

##### Error: `JSONDecodeError`

```
❌ CORS configuration error: Expecting value: line 1 column 1 (char 0)
```

**Cause:** `CORS_ORIGINS` is not valid JSON

**Wrong:**

```
CORS_ORIGINS=http://localhost:5173,https://*.vercel.app
```

**Correct:**

```
CORS_ORIGINS=["http://localhost:5173","https://*.vercel.app"]
```

---

##### Error: `AttributeError` or `TypeError`

```
❌ CORS configuration error: 'str' object has no attribute 'split'
```

**Cause:** `CORS_ORIGINS` format issue

**Solution:** Use exact JSON array format with double quotes

---

#### Case 3: Fallback Message Appears

**Problem:** Config failed, backend is allowing ALL origins (`*`)

**Issue:** This causes the credentials error you saw earlier

**Solution:** Fix `CORS_ORIGINS` format in Railway

---

### Step 4: Verify Environment Variables

In Railway Variables tab, you should have:

```
ENVIRONMENT=production
CORS_ORIGINS=["http://localhost:5173","https://*.vercel.app"]
```

**CRITICAL:**

- ✅ Use **double quotes** `"` not single quotes `'`
- ✅ Use **square brackets** `[ ]`
- ✅ **No spaces** after commas (optional but cleaner)
- ✅ Must be **valid JSON array**

---

## 🧪 Test CORS_ORIGINS Format Locally

You can test if your format is valid JSON:

### Python Test:

```python
import json

# Test your CORS_ORIGINS value
cors_value = '["http://localhost:5173","https://*.vercel.app"]'

try:
    result = json.loads(cors_value)
    print("✅ Valid JSON!")
    print(f"Parsed: {result}")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}")
```

### Online JSON Validator:

1. Go to https://jsonlint.com/
2. Paste your `CORS_ORIGINS` value
3. Click "Validate JSON"
4. Should show: **Valid JSON**

---

## 📋 Checklist

After updating Railway variables:

- [ ] Check Railway logs for CORS messages
- [ ] Verify no error messages appear
- [ ] See production mode message with correct pattern
- [ ] Test login from Vercel
- [ ] Check browser console - CORS error should be gone

---

## 🔧 Quick Fixes

### Fix 1: Simplify CORS (Testing Only)

If you just want to test if everything else works:

```
CORS_ORIGINS=["https://*.vercel.app"]
```

This removes localhost, but allows all Vercel deployments.

---

### Fix 2: Use Exact URL (No Wildcard)

If wildcard is causing issues:

```
CORS_ORIGINS=["http://localhost:5173","https://p2h-dvv5udqyz-naufals-projects-6b92b323.vercel.app"]
```

⚠️ **Warning:** Will break when Vercel creates new deployment

---

### Fix 3: Temporary Development Mode

For urgent testing only:

```
ENVIRONMENT=development
```

⚠️ **WARNING:** This allows ALL origins - **DO NOT USE IN PRODUCTION!**

---

## 📞 What to Share for Help

If still having issues, share:

1. **Railway Logs** - Copy the CORS-related messages
2. **Environment Variables** - Screenshot of Variables tab (hide sensitive values)
3. **Browser Console Error** - Full error message
4. **Network Tab** - Response headers from failed request

---

**Last Updated:** 2026-01-25
