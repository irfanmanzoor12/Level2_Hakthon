# 🚀 Deploy Frontend to Vercel RIGHT NOW

Your backend is **LIVE** at: `https://level2hakthon-production.up.railway.app`

## ✅ What's Already Done

- ✅ Backend deployed to Railway
- ✅ All API endpoints tested and working
- ✅ Database connected
- ✅ Frontend configured with Railway backend URL
- ✅ API client updated with correct endpoints

## 🎯 Deploy to Vercel in 3 Steps

### Option A: Using Vercel Dashboard (Easiest - 2 minutes)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/new
   - Login with GitHub

2. **Import Your Repository**
   - Click "Import Project"
   - Select: `irfanmanzoor12/Level2_Hakthon`
   - **Root Directory:** `frontend`
   - **Framework Preset:** Next.js (auto-detected)

3. **Set Environment Variable**
   - Click "Environment Variables"
   - Add:
     - **Name:** `NEXT_PUBLIC_API_URL`
     - **Value:** `https://level2hakthon-production.up.railway.app`
   - Click "Deploy"

4. **Wait 1-2 minutes** for deployment to complete!

---

### Option B: Using Vercel CLI (For developers)

```bash
# 1. Install Vercel CLI (if not installed)
npm install -g vercel

# 2. Navigate to frontend
cd frontend

# 3. Login to Vercel
vercel login

# 4. Deploy
vercel --prod

# When prompted:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No (first time) or Yes (if you've deployed before)
# - What's your project's name? level2-hakthon-frontend (or your choice)
# - In which directory is your code located? ./ (current directory)
# - Want to override settings? No (or Yes if you need to)
```

## 🔧 After Deployment

Once Vercel deployment completes:

1. **Copy your Vercel URL** (e.g., `https://level2-hakthon-frontend.vercel.app`)

2. **Update Backend CORS**
   - Go to Railway Dashboard → Your Backend Service → Variables
   - Find `CORS_ORIGINS`
   - Update to: `https://level2hakthon-production.up.railway.app,http://localhost:3000,https://YOUR-VERCEL-URL.vercel.app`
   - Replace `YOUR-VERCEL-URL` with your actual Vercel URL
   - Railway will auto-redeploy

3. **Test Your App!**
   - Open your Vercel URL
   - Register a new user
   - Create some tasks
   - Everything should work!

## 📋 Troubleshooting

### Issue: "Network Error" or "Failed to fetch"
**Solution:** Check CORS settings in Railway
- Make sure your Vercel URL is in the `CORS_ORIGINS` variable
- Format: `https://your-app.vercel.app` (no trailing slash)

### Issue: "API URL undefined"
**Solution:** Check environment variable in Vercel
- Go to Vercel Dashboard → Your Project → Settings → Environment Variables
- Verify `NEXT_PUBLIC_API_URL` is set to `https://level2hakthon-production.up.railway.app`
- Redeploy if you just added it

### Issue: Build fails
**Solution:**
- Check build logs in Vercel dashboard
- Make sure all dependencies are in `package.json`
- Verify Node version compatibility

## ✅ Success Criteria

Your deployment is successful when:
- ✅ Vercel build completes without errors
- ✅ Frontend loads in browser
- ✅ You can register a new user
- ✅ You can login
- ✅ You can create, view, update, and delete tasks
- ✅ No CORS errors in browser console

## 🎉 What's Next?

After deployment:
1. Share your Vercel URL with teammates
2. Test all features thoroughly
3. Monitor Railway and Vercel dashboards for any errors
4. Consider adding a custom domain (optional)

---

**Need help?** Check the full guide: `VERCEL_DEPLOY.md`
