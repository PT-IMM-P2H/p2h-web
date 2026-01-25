# 🌐 Flexible CORS Configuration Guide

## 📋 Overview

The backend now supports **environment-aware CORS** with **wildcard pattern matching** to handle Vercel's dynamic deployment URLs without constant Railway configuration updates.

---

## 🎯 How It Works

### Development Mode

```python
ENVIRONMENT = "development"
```

- **Allows ALL origins** (`*`)
- No need to configure specific URLs
- Perfect for local development

### Production Mode

```python
ENVIRONMENT = "production"
```

- Uses configured `CORS_ORIGINS` from environment variables
- Supports **wildcard patterns** for dynamic URLs
- Maintains security by only allowing specified domains

---

## 🔧 Configuration Options

### Option 1: Exact URLs (Current Setup)

```json
CORS_ORIGINS = ["http://localhost:5173", "https://p2h-bro0xl7kq-naufals-projects-6b92b323.vercel.app"]
```

**Pros:**

- ✅ Most secure
- ✅ Explicit control

**Cons:**

- ❌ Need to update for each new Vercel deployment
- ❌ Preview deployments won't work

---

### Option 2: Wildcard for Vercel (Recommended)

```json
CORS_ORIGINS = ["http://localhost:5173", "https://*.vercel.app"]
```

**Pros:**

- ✅ Works with ALL Vercel deployments (production, preview, development)
- ✅ No need to update Railway for each deployment
- ✅ Still secure (only allows Vercel domains)

**Cons:**

- ⚠️ Allows any Vercel deployment (including other projects if someone knows your API URL)

---

### Option 3: Specific Vercel Project Wildcard (Most Balanced)

```json
CORS_ORIGINS = ["http://localhost:5173", "https://p2h-*.vercel.app"]
```

**Pros:**

- ✅ Works with all deployments of your specific project
- ✅ More secure than full wildcard
- ✅ No updates needed for preview deployments

**Cons:**

- ⚠️ Requires your Vercel project to have consistent naming

---

### Option 4: Multiple Wildcards

```json
CORS_ORIGINS = [
  "http://localhost:5173",
  "https://p2h-*.vercel.app",
  "https://*.railway.app",
  "https://yourdomain.com"
]
```

**Pros:**

- ✅ Maximum flexibility
- ✅ Supports multiple deployment platforms
- ✅ Can mix exact URLs and wildcards

---

## 🚀 How to Update Railway

### Step 1: Go to Railway Dashboard

https://railway.app/dashboard

### Step 2: Select Backend Project

Click on your FastAPI backend project

### Step 3: Update CORS_ORIGINS Variable

**For Vercel Wildcard (Recommended):**

```json
["http://localhost:5173", "https://*.vercel.app"]
```

**For Specific Project Wildcard:**

```json
["http://localhost:5173", "https://p2h-*.vercel.app"]
```

**For Current Deployment Only:**

```json
[
  "http://localhost:5173",
  "https://p2h-bro0xl7kq-naufals-projects-6b92b323.vercel.app"
]
```

### Step 4: Save & Wait for Redeploy

Railway will automatically redeploy (1-2 minutes)

---

## 🧪 Testing

### Test Wildcard Pattern Locally

You can test if a pattern matches using Python:

```python
import re

def test_cors_pattern(pattern, url):
    regex_pattern = pattern.replace(".", r"\.").replace("*", ".*")
    match = re.match(f"^{regex_pattern}$", url)
    return match is not None

# Test examples
print(test_cors_pattern("https://*.vercel.app", "https://p2h-xyz.vercel.app"))  # True
print(test_cors_pattern("https://p2h-*.vercel.app", "https://p2h-abc.vercel.app"))  # True
print(test_cors_pattern("https://p2h-*.vercel.app", "https://other-abc.vercel.app"))  # False
```

---

## 📊 Pattern Examples

| Pattern                    | Matches                         | Doesn't Match                  |
| -------------------------- | ------------------------------- | ------------------------------ |
| `https://*.vercel.app`     | `https://anything.vercel.app`   | `https://vercel.app`           |
| `https://p2h-*.vercel.app` | `https://p2h-abc123.vercel.app` | `https://other-abc.vercel.app` |
| `https://*.example.com`    | `https://api.example.com`       | `https://example.com`          |
| `https://*-staging.app`    | `https://p2h-staging.app`       | `https://p2h-production.app`   |

---

## 🔒 Security Considerations

### ✅ Safe Wildcards

```json
["https://p2h-*.vercel.app"]  // Only your project
["https://*.yourdomain.com"]  // Only your domain
```

### ⚠️ Use with Caution

```json
["https://*.vercel.app"]  // Any Vercel project
["https://*"]             // Any HTTPS site (DON'T USE!)
```

### ❌ Never Use

```json
["*"] // Allows ANY origin (development only!)
```

---

## 🐛 Troubleshooting

### CORS Error Still Appears

1. **Check Railway Logs**
   - Look for CORS log message on startup
   - Should show: `🔒 CORS: Production mode with wildcard - pattern: ...`

2. **Verify Environment Variable**
   - Make sure `ENVIRONMENT=production` in Railway
   - Check `CORS_ORIGINS` is set correctly

3. **Clear Browser Cache**
   - Hard refresh: `Ctrl+Shift+R`
   - Or open in incognito mode

4. **Check Pattern Syntax**
   - Must use double quotes `"` not single quotes `'`
   - Must be valid JSON array format

### Pattern Not Matching

1. **Test Pattern Locally** (see Testing section above)
2. **Check for Typos** in the pattern
3. **Verify URL Format** (include `https://` prefix)

---

## 📝 Example Railway Configuration

### Minimal Setup (Vercel Only)

```
ENVIRONMENT=production
CORS_ORIGINS=["https://*.vercel.app"]
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
```

### Recommended Setup (Multiple Environments)

```
ENVIRONMENT=production
CORS_ORIGINS=["http://localhost:5173","https://p2h-*.vercel.app","https://yourdomain.com"]
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
```

---

## 🎓 Summary

1. **Development**: Uses `*` (allow all) - no configuration needed
2. **Production**: Uses `CORS_ORIGINS` with wildcard support
3. **Recommended**: Use `https://*.vercel.app` or `https://p2h-*.vercel.app`
4. **Update Once**: Set in Railway and forget about it!

---

## 🔗 Related Files

- [`app/main.py`](file:///e:/Magang/Github-P2H-web/p2h-web/backend/app/main.py#L125-L169) - CORS middleware configuration
- [`app/config.py`](file:///e:/Magang/Github-P2H-web/p2h-web/backend/app/config.py#L33-L67) - Settings and wildcard pattern matching

---

**Last Updated:** 2026-01-25
