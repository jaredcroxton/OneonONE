# PerformOS Zeabur Deployment Checklist

## ✅ Pre-Deployment Verification

### Backend Structure
- [x] Separate `/backend` folder with all Python code
- [x] `requirements.txt` with all dependencies
- [x] `zeabur.json` with build/run configuration
- [x] `.env.example` for reference
- [x] Server binds to `0.0.0.0` and uses PORT from environment
- [x] CORS configured for production domains
- [x] All environment variables read from `os.getenv()`

### Frontend Structure
- [x] Separate `/frontend` folder with React app
- [x] `package.json` with build scripts
- [x] `zeabur.json` with build/run configuration
- [x] `.env.example` for reference
- [x] API calls use `REACT_APP_BACKEND_URL` environment variable
- [x] No hardcoded localhost URLs
- [x] Build output directory: `build`

### Database
- [x] MongoDB Atlas cluster created
- [x] Network access configured (0.0.0.0/0 for Zeabur)
- [x] Database user created
- [x] Connection string obtained

## 📋 Deployment Steps

### Step 1: Push to GitHub
```bash
# Ensure all changes are committed
git add .
git commit -m "Zeabur deployment configuration"
git push origin main
```

### Step 2: Deploy Backend to Zeabur

1. **Create Backend Service**:
   - Service Type: Web Service
   - Framework: Python
   - Root Directory: `/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port ${PORT}`

2. **Add Backend Environment Variables**:
   ```
   MONGO_URL=mongodb+srv://performos_admin:Welcome2026!@oneonone.kzrqgka.mongodb.net/performos?retryWrites=true&w=majority
   DB_NAME=performos
   JWT_SECRET=performos_jwt_secret_prod_2026
   OPENAI_API_KEY=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
   ALLOWED_ORIGINS=https://performos.digital,https://your-frontend-url.zeabur.app
   ```

3. **Deploy Backend**:
   - Click Deploy
   - Wait for build to complete
   - Copy the backend URL (e.g., `https://backend-abc123.zeabur.app`)

### Step 3: Deploy Frontend to Zeabur

1. **Create Frontend Service**:
   - Service Type: Static
   - Framework: Create React App
   - Root Directory: `/frontend`
   - Build Command: `yarn install && yarn build`
   - Start Command: `npx serve -s build -l ${PORT}`
   - Output Directory: `build`

2. **Add Frontend Environment Variables**:
   ```
   REACT_APP_BACKEND_URL=https://backend-abc123.zeabur.app
   ```
   (Use the actual backend URL from Step 2)

3. **Deploy Frontend**:
   - Click Deploy
   - Wait for build to complete

### Step 4: Link Custom Domain

1. **Add Domain to Frontend Service**:
   - Go to frontend service settings
   - Add domain: `performos.digital`
   - Copy the CNAME/A records

2. **Update DNS**:
   - Go to your domain registrar
   - Add the DNS records provided by Zeabur
   - Wait for DNS propagation (5-30 minutes)

3. **Update Backend CORS** (if needed):
   - Add `performos.digital` to `ALLOWED_ORIGINS` in backend environment variables
   - Redeploy backend

### Step 5: Seed Database

After successful deployment, seed the database with demo data:

**Option A: Using curl**:
```bash
curl -X POST https://your-backend-url.zeabur.app/api/seed
```

**Option B: Using Zeabur Console**:
1. Open backend service console
2. Run: `python3 -c "from seed_data import seed_database; import asyncio; asyncio.run(seed_database())"`

### Step 6: Test the Application

1. **Test Login**:
   - Go to `https://performos.digital`
   - Try logging in with:
     - Manager: alex@performos.io / demo
     - Executive: rachel@performos.io / demo
     - Team Member: ashley@performos.io / demo

2. **Test AI Features**:
   - Manager dashboard → AI Briefing
   - Manager dashboard → My Coaching
   - Executive dashboard → AI Executive Summary

3. **Verify Backend API**:
   ```bash
   curl https://your-backend-url.zeabur.app/api/schedule/weeks
   ```

## 🔧 Troubleshooting

### Frontend shows "Failed to fetch"
- Check `REACT_APP_BACKEND_URL` is set correctly in frontend env vars
- Verify backend is running and accessible
- Check browser console for CORS errors

### CORS errors
- Add frontend URL to `ALLOWED_ORIGINS` in backend
- Redeploy backend after updating environment variables

### Database connection fails
- Verify `MONGO_URL` is correct
- Check MongoDB Atlas network access (whitelist 0.0.0.0/0)
- Verify database user credentials

### Build fails on Zeabur
- Check build logs in Zeabur console
- Verify `zeabur.json` configuration
- Ensure all dependencies are in requirements.txt / package.json

## 📊 Service URLs Structure

After deployment, you'll have:
- **Backend API**: `https://backend-xyz.zeabur.app`
- **Frontend Preview**: `https://frontend-xyz.zeabur.app`
- **Custom Domain**: `https://performos.digital` (points to frontend)

## 🔄 Future Updates

To update the application:

1. **Make changes in Emergent**
2. **Commit to GitHub**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
3. **Zeabur auto-deploys** both services
4. **No manual configuration needed** after initial setup

## 🎯 Environment Variables Summary

### Backend (Required)
| Variable | Description | Example |
|----------|-------------|---------|
| MONGO_URL | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| DB_NAME | Database name | `performos` |
| JWT_SECRET | Secret for JWT tokens | `your_secure_secret_here` |
| OPENAI_API_KEY | OpenAI API key for AI features | `sk-proj-...` |
| ALLOWED_ORIGINS | CORS allowed origins (comma-separated) | `https://performos.digital,https://frontend.zeabur.app` |

### Frontend (Required)
| Variable | Description | Example |
|----------|-------------|---------|
| REACT_APP_BACKEND_URL | Backend API base URL | `https://backend-xyz.zeabur.app` |

## ✅ Final Checklist

Before going live:
- [ ] Backend deployed and healthy
- [ ] Frontend deployed and healthy
- [ ] Custom domain linked and DNS propagated
- [ ] Database seeded with demo users
- [ ] All three user roles can log in
- [ ] AI features working (OpenAI API key valid)
- [ ] No console errors in browser
- [ ] API calls successful (check Network tab)
- [ ] CORS configured correctly
- [ ] HTTPS enabled on both services

## 🆘 Support

If deployment fails:
1. Check Zeabur build logs for specific errors
2. Verify all environment variables are set
3. Test backend API directly with curl
4. Check MongoDB Atlas connection from Zeabur IP
5. Review CORS configuration for frontend domain
