# Frontend Deployment Guide (Vercel)

## Overview
This guide covers deploying the Next.js frontend to Vercel (recommended) or other platforms.

## Prerequisites
- Backend deployed to Railway (see RAILWAY_DEPLOY.md)
- Backend URL available (e.g., `https://your-app.railway.app`)
- Vercel account (free tier works)

## Configuration Files
- `frontend/package.json` - Dependencies and scripts
- `frontend/next.config.js` - Next.js configuration
- `frontend/.env.local.example` - Environment variables template

## Required Environment Variables

Set these in your deployment platform:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-app.railway.app` |
| `NEXT_PUBLIC_APP_URL` | Frontend URL (optional) | `https://your-app.vercel.app` |

**Important:**
- Use `NEXT_PUBLIC_` prefix for client-side env variables in Next.js
- No trailing slash in URLs
- Must use HTTPS in production

## Deployment Steps

### Option A: Deploy with Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Login to Vercel**
   ```bash
   vercel login
   ```

4. **Deploy**
   ```bash
   # Preview deployment
   vercel

   # Production deployment
   vercel --prod
   ```

5. **Set environment variables** (during first deploy or via dashboard)
   ```bash
   # During deploy, Vercel will prompt for:
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```

### Option B: Deploy via Vercel Dashboard

1. **Connect GitHub Repository**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Select the repository

2. **Configure Project**
   - Framework Preset: **Next.js** (auto-detected)
   - Root Directory: **`frontend`** (important!)
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

3. **Set Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add:
     - Key: `NEXT_PUBLIC_API_URL`
     - Value: `https://your-backend.railway.app`
   - Save

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

## Post-Deployment Configuration

### Update Backend CORS

After deploying frontend, update Railway backend environment variables:

1. Go to Railway → Your Service → Variables
2. Update `CORS_ORIGINS` to include your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```
3. Redeploy backend

### Test Deployment

1. **Visit your frontend URL**
   - Example: `https://your-app.vercel.app`

2. **Test user registration**
   - Click "Create new account"
   - Register with email/password
   - Should redirect to tasks page

3. **Test task operations**
   - Create a new task
   - Mark as complete
   - Edit task
   - Delete task

4. **Check browser console**
   - No CORS errors
   - No 401/403 errors
   - API calls successful

## Troubleshooting

### CORS Errors
**Problem:** `Access to fetch at 'https://...' has been blocked by CORS policy`

**Solution:**
1. Verify `CORS_ORIGINS` in Railway includes your Vercel URL
2. No trailing slash: `https://app.vercel.app` ✓, `https://app.vercel.app/` ✗
3. Must match exactly (including protocol)
4. Redeploy backend after changing CORS_ORIGINS

### Environment Variable Not Working
**Problem:** API URL is localhost in production

**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` is set in Vercel
2. Check variable name has `NEXT_PUBLIC_` prefix
3. Redeploy after adding variables
4. Check build logs for variable values

### 404 on API Calls
**Problem:** API endpoints return 404

**Solution:**
1. Verify backend is deployed and running
2. Check backend URL in `NEXT_PUBLIC_API_URL`
3. Test backend health: `https://your-backend.railway.app/api/health`
4. Verify backend routes match frontend API calls

### Build Fails
**Problem:** Vercel build fails

**Solution:**
1. Check build logs in Vercel dashboard
2. Verify `package.json` has all dependencies
3. Try local build: `cd frontend && npm run build`
4. Check TypeScript errors: `npm run lint`

### Authentication Not Persisting
**Problem:** User logged out on page refresh

**Solution:**
1. Check browser localStorage has `token` and `user`
2. Verify JWT token is valid (not expired)
3. Check backend JWT_EXPIRATION_DAYS setting
4. Try clearing browser cache/localStorage

## Local Development with Production Backend

To test frontend locally with production backend:

1. **Create `.env.local` in frontend/**
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```

2. **Update backend CORS to allow localhost**
   - Railway → Variables → CORS_ORIGINS
   - Add: `http://localhost:3000`

3. **Run frontend**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Test at** `http://localhost:3000`

## Alternative Platforms

### Deploy to Netlify

1. **Connect repository**
   - Go to [netlify.com](https://netlify.com)
   - Import from Git

2. **Configure**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/.next`

3. **Environment variables**
   - Add `NEXT_PUBLIC_API_URL`

4. **Deploy**

### Deploy to Railway (Alternative)

If you want both frontend and backend on Railway:

1. **Create new Railway service**
2. **Set root directory** to `frontend`
3. **Set environment variables**
4. Railway auto-detects Next.js

## Continuous Deployment

### Automatic Deploys (Vercel + GitHub)

Vercel automatically deploys:
- **Production:** Pushes to `main` branch
- **Preview:** Pull requests and other branches

### Manual Triggers

- Vercel Dashboard → Deployments → Redeploy
- Or use CLI: `cd frontend && vercel --prod`

## Custom Domain (Optional)

1. **Add domain in Vercel**
   - Project Settings → Domains
   - Add your domain
   - Configure DNS records

2. **Update environment variables**
   - Update `NEXT_PUBLIC_APP_URL`
   - Update backend `CORS_ORIGINS`

## Monitoring and Logs

- **Vercel Dashboard:** Real-time logs and metrics
- **Browser DevTools:** Network tab for API calls
- **Railway Dashboard:** Backend logs

## Success Checklist

- [ ] Frontend deployed and accessible
- [ ] Environment variables set correctly
- [ ] Backend CORS includes frontend URL
- [ ] User registration works
- [ ] User login works
- [ ] Tasks CRUD operations work
- [ ] No console errors
- [ ] No CORS errors
- [ ] Authentication persists on refresh
- [ ] Mobile responsive (test viewport)

## Performance Optimization (Optional)

1. **Enable Vercel Analytics**
   - Project Settings → Analytics
   - Track real user metrics

2. **Add caching headers**
   - Configure in `next.config.js`

3. **Optimize images**
   - Use Next.js `<Image>` component

4. **Add loading states**
   - Already implemented in code

---

**Next Steps:**
- Deploy backend to Railway first (RAILWAY_DEPLOY.md)
- Then deploy frontend using this guide
- Test end-to-end functionality
- Share your app URL!
