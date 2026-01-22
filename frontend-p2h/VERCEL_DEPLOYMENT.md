# Vercel Deployment Guide - PT-IMM P2H System

## Prerequisites
1. GitHub account
2. Vercel account (free tier available at https://vercel.com)
3. Code pushed to GitHub repository

## Deployment Steps

### 1. Prepare Environment Variables
Before deploying, prepare these environment variables for Vercel:

```bash
VITE_API_BASE_URL=https://your-backend-api.com
VITE_APP_NAME=P2H System
VITE_APP_VERSION=1.0.0
VITE_TOKEN_EXPIRY=30
VITE_REFRESH_TOKEN_BEFORE=5
VITE_DEFAULT_LANGUAGE=id
VITE_TIMEZONE=Asia/Jakarta
VITE_ENABLE_TELEGRAM=false
```

### 2. Deploy to Vercel

#### Option A: Using Vercel Dashboard (Recommended)
1. Go to https://vercel.com and login
2. Click "Add New..." → "Project"
3. Import your GitHub repository (PT-IMM-P2H)
4. Configure build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend-p2h`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
5. Add environment variables from step 1
6. Click "Deploy"

#### Option B: Using Vercel CLI
```bash
# Install Vercel CLI globally
npm install -g vercel

# Navigate to frontend directory
cd frontend-p2h

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### 3. Post-Deployment Configuration

#### Update CORS on Backend
Add your Vercel domain to backend CORS settings in `backend/app/main.py`:
```python
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://your-app.vercel.app",  # Add this
]
```

#### Configure Custom Domain (Optional)
1. In Vercel Dashboard → Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### 4. Verification Checklist
After deployment, test these features:
- ✅ Login page loads correctly
- ✅ Sidebar navigation works
- ✅ Dashboard displays data (if backend connected)
- ✅ All tables are responsive on mobile
- ✅ Form P2H works properly
- ✅ Riwayat user displays correctly
- ✅ All admin features accessible
- ✅ Responsive on mobile devices (burger menu, tables, forms)

### 5. Common Issues & Solutions

#### Issue: API Requests Fail
**Solution**: Check `VITE_API_BASE_URL` environment variable points to correct backend URL

#### Issue: 404 on Page Refresh
**Solution**: `vercel.json` should have SPA rewrite rule (already configured)

#### Issue: Images Not Loading
**Solution**: Ensure images are in `public/` directory, not `src/assets/`

#### Issue: Build Fails
**Solution**: 
- Check `package.json` has correct dependencies
- Ensure all imports are correct
- Run `npm run build` locally first to catch errors

### 6. Continuous Deployment
Vercel automatically redeploys when you push to main branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### 7. Environment-Specific Deployments

#### Production
- Branch: `main`
- Domain: `your-app.vercel.app`
- API: Production backend

#### Staging/Preview
- Any other branch
- Auto-generated preview URL
- API: Staging backend (configure via environment variables)

## Important Notes
1. **Backend API**: Make sure backend is deployed and accessible (e.g., on Railway, Render, or Heroku)
2. **Environment Variables**: Never commit `.env` file to Git
3. **Build Time**: First deployment takes 2-5 minutes
4. **Free Tier Limits**: 
   - 100 GB bandwidth/month
   - 6,000 build minutes/month
   - Unlimited preview deployments

## Support & Resources
- Vercel Documentation: https://vercel.com/docs
- Vite Documentation: https://vitejs.dev/guide/
- Vue Router: https://router.vuejs.org/
