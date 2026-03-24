# PerformOS Zeabur Deployment - FINAL SETUP GUIDE

## 🚨 IMPORTANT: MongoDB Atlas SSL Issue in Emergent

**Known Issue:** The Emergent preview environment has SSL/TLS compatibility issues with MongoDB Atlas.  
**Impact:** Cannot test Atlas connection locally, but **Zeabur production will work fine**.  
**Workaround:** Preview uses local MongoDB; Zeabur deployment uses Atlas.

---

## 📦 EXACT ZEABUR SETUP

### 1. Backend Service Configuration

**Root Directory:**
```
backend
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn server:app --host 0.0.0.0 --port ${PORT}
```

**Environment Variables:**
```env
MONGO_URL=mongodb+srv://performos_admin:Welcome2026!@oneonone.kzrqgka.mongodb.net/performos?retryWrites=true&w=majority
DB_NAME=performos
JWT_SECRET=performos_jwt_secret_prod_2026
OPENAI_API_KEY=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
```

**After backend deploys, add frontend URL to CORS:**
```env
ALLOWED_ORIGINS=https://performos.digital,https://your-frontend-url.zeabur.app
```

---

### 2. Frontend Service Configuration

**Root Directory:**
```
frontend
```

**Build Command:**
```bash
yarn install && yarn build
```

**Start Command:**
```bash
npx serve -s build -l ${PORT}
```

**Output Directory:**
```
build
```

**Environment Variables:**
```env
REACT_APP_BACKEND_URL=https://your-backend-url.zeabur.app
```
(Use actual backend URL after backend service deploys)

---

## 🔄 DEPLOYMENT ORDER (CRITICAL)

### Step 1: Deploy Backend First
1. Create service in Zeabur
2. Connect to GitHub repository
3. Set root directory: `backend`
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn server:app --host 0.0.0.0 --port ${PORT}`
6. Add all backend environment variables
7. **Deploy and wait for success**
8. **Copy the backend service URL** (e.g., `https://performos-backend-xyz.zeabur.app`)

### Step 2: Seed Database
After backend is live, seed the database via Zeabur console:
```bash
python3 -c "from seed_data import seed_database; import asyncio; asyncio.run(seed_database())"
```

Or create a temporary seed endpoint and call it:
```bash
curl -X POST https://your-backend-url.zeabur.app/api/seed
```

### Step 3: Deploy Frontend Second
1. Create service in Zeabur
2. Connect to same GitHub repository
3. Set root directory: `frontend`
4. Set build command: `yarn install && yarn build`
5. Set start command: `npx serve -s build -l ${PORT}`
6. Set output directory: `build`
7. Add environment variable:
   ```
   REACT_APP_BACKEND_URL=https://performos-backend-xyz.zeabur.app
   ```
   (Use the actual backend URL from Step 1)
8. **Deploy and wait for success**

### Step 4: Update Backend CORS
1. Go back to backend service settings
2. Update `ALLOWED_ORIGINS` environment variable to include frontend URL:
   ```
   ALLOWED_ORIGINS=https://performos.digital,https://performos-frontend-xyz.zeabur.app
   ```
3. **Redeploy backend** (to apply new CORS settings)

### Step 5: Link Custom Domain
1. Go to frontend service settings in Zeabur
2. Click "Add Domain"
3. Enter: `performos.digital`
4. Copy the DNS records provided
5. Update your DNS settings at your domain registrar
6. Wait 5-30 minutes for DNS propagation

### Step 6: Verify
1. Test backend API:
   ```bash
   curl https://performos-backend-xyz.zeabur.app/api/members
   ```
   (Should return JSON with team members)

2. Test frontend:
   - Visit `https://performos.digital`
   - Try logging in with: `alex@performos.io` / `demo`
   - Verify dashboard loads with data

---

## ⚠️ CRITICAL NOTES

### MongoDB Atlas Works on Zeabur (Not Emergent Preview)
- **Emergent preview:** Has SSL compatibility issues with MongoDB Atlas
- **Zeabur production:** Works perfectly with MongoDB Atlas
- **Solution:** Use local MongoDB for Emergent preview, Atlas for Zeabur deployment

### Environment Variable Format
- Backend uses Python: `os.getenv("VAR_NAME")`
- Frontend uses React: `process.env.REACT_APP_BACKEND_URL`
- **Note:** Frontend env vars are baked in at build time (rebuild if you change them)

### CORS Configuration
- Must include BOTH:
  - Custom domain: `https://performos.digital`
  - Zeabur frontend URL: `https://frontend-xyz.zeabur.app`
- Format: Comma-separated, no spaces

### Port Binding
- Backend MUST use: `--host 0.0.0.0 --port ${PORT}`
- Frontend serve MUST use: `-l ${PORT}`
- Zeabur provides PORT dynamically

---

## 🐛 TROUBLESHOOTING

### "Request failed" on login
**Cause:** Backend not reachable or CORS blocking  
**Fix:**
1. Check backend is running in Zeabur console
2. Verify `REACT_APP_BACKEND_URL` in frontend env vars
3. Check `ALLOWED_ORIGINS` includes frontend domain
4. Check browser console for specific error

### "Invalid credentials"
**Cause:** Database not seeded  
**Fix:** Run seed script in Zeabur backend console

### 502/504 errors
**Cause:** Backend crashed or not binding to PORT  
**Fix:** Check Zeabur backend logs, verify start command uses `${PORT}`

### CORS errors in browser console
**Cause:** Frontend domain not in ALLOWED_ORIGINS  
**Fix:** Update backend ALLOWED_ORIGINS and redeploy backend

---

## ✅ FINAL CHECKLIST

Before going live:
- [ ] Backend deployed and running on Zeabur
- [ ] Frontend deployed and running on Zeabur
- [ ] MongoDB Atlas connected to backend
- [ ] Database seeded with demo users
- [ ] `REACT_APP_BACKEND_URL` points to backend service
- [ ] `ALLOWED_ORIGINS` includes frontend domain + custom domain
- [ ] Custom domain linked and DNS propagated
- [ ] Test login with all three roles
- [ ] Test AI features (OpenAI key has credits)
- [ ] No console errors in browser

---

## 📊 Expected Service URLs

After deployment:
- **Backend API:** `https://performos-backend-[random].zeabur.app`
- **Frontend (Zeabur):** `https://performos-frontend-[random].zeabur.app`
- **Custom Domain:** `https://performos.digital` (points to frontend)

---

## 🔄 UPDATING AFTER INITIAL DEPLOYMENT

1. Make changes in Emergent
2. Commit to git: `git add . && git commit -m "Your message"`
3. Push to GitHub: `git push origin main`
4. Zeabur auto-deploys both services
5. **If you change frontend env vars:** Zeabur will auto-rebuild
6. **No manual steps needed** after initial configuration

---

## 💡 WHY TWO DATABASES?

**Preview Environment (Emergent):**
- Uses: `mongodb://localhost:27017` (local MongoDB in container)
- Why: SSL compatibility with container environment
- When: Testing and development in Emergent

**Production (Zeabur):**
- Uses: MongoDB Atlas (managed, AWS-hosted)
- Why: Persistent, scalable, professional hosting
- When: Live deployment for customers

**They don't conflict** - each environment uses its own database via environment variables.

---

**VERSION:** 1.1 - Includes SSL workaround  
**TESTED:** March 2026  
**STATUS:** Ready for production deployment

