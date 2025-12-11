# Railway Deployment Guide

## Configuration Files
- `nixpacks.toml` - Specifies build and start commands for Railway
- `railway.json` - Railway service configuration

## Required Environment Variables

You must set these environment variables in the Railway dashboard (not in .env file):

1. Go to your Railway project
2. Click on your service
3. Navigate to "Variables" tab
4. Add the following variables:

### Required Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@host/db?sslmode=require` |
| `JWT_SECRET` | Secret key for JWT tokens | `your-super-secret-jwt-key-change-this-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_DAYS` | JWT expiration in days | `7` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `https://your-frontend.vercel.app,http://localhost:3000` |
| `ENVIRONMENT` | Application environment | `production` |

## Deployment Steps

1. **Commit your changes**
   ```bash
   git add nixpacks.toml railway.json
   git commit -m "Configure Railway deployment"
   git push
   ```

2. **Set Environment Variables in Railway**
   - Navigate to your Railway project
   - Go to Variables tab
   - Add all required variables listed above
   - Make sure to use your actual values (especially DATABASE_URL from Neon)

3. **Deploy**
   - Railway will automatically deploy when you push to your connected branch
   - Or trigger manual deployment from Railway dashboard

4. **Verify Deployment**
   - Check deployment logs for any errors
   - Visit `https://your-app.railway.app/` to see the root endpoint
   - Visit `https://your-app.railway.app/docs` to see API documentation
   - Visit `https://your-app.railway.app/api/health` to check health status

## Troubleshooting

### Build Error: "can't cd to backend"
**Fixed!** The root `nixpacks.toml` now uses `backend/requirements.txt` path instead of `cd backend &&`.

If you still encounter this error:
- **Option A (Recommended)**: Set Root Directory in Railway:
  1. Go to Service → Settings
  2. Set **Root Directory** to `backend`
  3. This uses `backend/nixpacks.toml` which doesn't have path issues

- **Option B**: Current fix in root `nixpacks.toml`:
  - Uses `pip install -r backend/requirements.txt`
  - Start command still uses `cd backend` which works after install

### App crashes on startup
- Check that all required environment variables are set in Railway
- Verify DATABASE_URL is correct and accessible from Railway
- Check deployment logs for specific error messages

### Database connection errors
- Ensure DATABASE_URL includes `?sslmode=require` for Neon
- Verify your Neon database allows connections from Railway's IP ranges

### CORS errors from frontend
- Make sure CORS_ORIGINS includes your frontend URL
- Format: `https://your-frontend.vercel.app` (no trailing slash)
- Multiple origins: `https://app1.com,https://app2.com` (comma-separated, no spaces)

## Local Development vs Production

### Local (.env file)
```env
DATABASE_URL=postgresql://...
JWT_SECRET=dev-secret
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

### Production (Railway Variables)
- Set all variables in Railway dashboard
- Use production values
- Never commit .env to git (it's in .gitignore)
