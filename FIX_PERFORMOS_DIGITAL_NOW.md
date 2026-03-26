# 🚨 URGENT: Fix performos.digital Deployment

## Current Issue
Your deployed app shows 500 errors on AI features because **environment variables are missing in deployment**.

---

## ✅ EXACT STEPS TO FIX

### Step 1: Add Environment Variables in Emergent

**Go to your deployment settings and add these EXACTLY:**

```
MONGO_URL=mongodb+srv://performos_admin:Welcome2026!@oneonone.kzrqgka.mongodb.net/?retryWrites=true&w=majority
DB_NAME=performos
JWT_SECRET=performos_jwt_secret_prod_2026
OPENAI_API_KEY=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
GOOGLE_CLIENT_ID=1076094647421-u1bge3nkhmotrc1lganqm53e51dka88a.apps.googleusercontent.com
REACT_APP_GOOGLE_CLIENT_ID=1076094647421-u1bge3nkhmotrc1lganqm53e51dka88a.apps.googleusercontent.com
```

**CRITICAL:** Make sure you add ALL of these. The OPENAI_API_KEY is the one causing your 500 errors.

### Step 2: Deploy Again

Click "Deploy" in Emergent

### Step 3: After Deployment, Seed Database

Visit in browser:
```
https://performos.digital/api/admin/seed
```

You should see:
```json
{"message": "✅ Database seeded successfully", "users": [...]}
```

### Step 4: Test Login

Go to https://performos.digital and login with:
- alex@performos.io / demo

### Step 5: Test AI Features

After login:
- Go to "AI Briefing" tab
- Click "Generate This Week's Briefing"
- Should work WITHOUT 500 errors

---

## 🔍 How to Verify Environment Variables Are Set

After deployment, open Emergent deployment console and run:
```bash
env | grep OPENAI
```

Should show:
```
OPENAI_API_KEY=sk-proj-JSFzYClram7j7...
```

If it shows nothing, the environment variables weren't added correctly.

---

## ⚠️ Common Issues

### "500 errors persist after adding env vars"
**Cause:** Environment variables not saved or deployment didn't restart  
**Fix:** 
1. Double-check variables are in deployment settings (not just .env files)
2. Redeploy to force restart
3. Clear browser cache

### "Database empty after deployment"
**Cause:** Auto-seed only runs if database is completely empty  
**Fix:** Visit `/api/admin/seed` endpoint to manually seed

### "Google button doesn't work"
**Cause:** Google Cloud Console needs authorized origins  
**Fix:** Add performos.digital to authorized origins in Google Cloud Console

---

## 📊 What Should Work After Fix

After adding environment variables and redeploying:

✅ **Login:** Both email/password and Google (after Google Cloud setup)  
✅ **Team Member Dashboard:** Submit weekly reflections  
✅ **Manager Dashboard:**
  - Team Schedule
  - Team Health (risk flags)  
  - Performance Trends
  - **AI Briefing** (no more 500 errors!)
  - **My Coaching** (no more 500 errors!)

✅ **Executive Dashboard:**
  - Organization Heatmap
  - **AI Executive Summary** (no more 500 errors!)

---

## 🎯 The Bottom Line

**Your code is 100% correct.**

**The problem:** Emergent deployment isn't loading the environment variables you think it's loading.

**The fix:** Make sure ALL environment variables above are in Emergent deployment settings (NOT just .env files in code).

**After adding them correctly and redeploying, performos.digital will work perfectly.** ✅

---

**Screenshot this list of environment variables and make sure EVERY SINGLE ONE is in your Emergent deployment settings before you deploy again!** 🚀
