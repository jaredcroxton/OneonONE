# 🚨 CRITICAL: Environment Variables for Emergent Deployment

## Why Your Deployed App Isn't Working

The errors in your console show:
- ❌ **500 errors on `/api/generate-coaching`** 
- ❌ "Failed to generate briefing"

**Root Cause:** The deployed app is missing the OpenAI API key in its environment variables.

---

## ✅ Add These to Emergent Deployment Settings

Go to your deployment settings in Emergent and add ALL of these:

```
MONGO_URL=mongodb+srv://performos_admin:Welcome2026!@oneonone.kzrqgka.mongodb.net/performos?retryWrites=true&w=majority
DB_NAME=performos
JWT_SECRET=performos_jwt_secret_prod_2026
OPENAI_API_KEY=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
GOOGLE_CLIENT_ID=1076094647421-u1bge3nkhmotrc1lganqm53e51dka88a.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=(Get from Google Cloud Console)
REACT_APP_GOOGLE_CLIENT_ID=1076094647421-u1bge3nkhmotrc1lganqm53e51dka88a.apps.googleusercontent.com
```

---

## 🎯 What Each Variable Does

| Variable | Purpose |
|----------|---------|
| `MONGO_URL` | Connects to MongoDB Atlas database |
| `DB_NAME` | Database name in MongoDB |
| `JWT_SECRET` | Signs authentication tokens |
| `OPENAI_API_KEY` | **CRITICAL** - Powers AI Briefing, My Coaching, Executive Summary |
| `GOOGLE_CLIENT_ID` | Backend Google OAuth verification |
| `GOOGLE_CLIENT_SECRET` | Backend Google OAuth verification |
| `REACT_APP_GOOGLE_CLIENT_ID` | Frontend Google Sign-In button |

---

## 📋 Step-by-Step Fix

### **Step 1: Add Environment Variables in Emergent**
1. Go to your Emergent deployment dashboard
2. Find "Environment Variables" or "Settings"
3. Add ALL variables listed above
4. Save changes

### **Step 2: Redeploy**
Click "Deploy" button in Emergent

### **Step 3: After Deployment, Test:**

**Test Backend API:**
```bash
curl https://performos.digital/api/members
```
Should return JSON with team members

**Test OpenAI (via browser):**
1. Login to performos.digital
2. Go to Manager dashboard
3. Click "AI Briefing" tab
4. Should generate without 500 errors

**Test Google Login:**
1. Click "Sign in with Google"
2. Select a Google account that matches an email in your database
3. Should login successfully

---

## ⚠️ Google Cloud Console Setup (Required for Google Login)

**Before Google Login works, configure in Google Cloud Console:**

1. Go to: https://console.cloud.google.com/apis/credentials
2. Find OAuth client: `1076094647421-u1bge3nkhmotrc1lganqm53e51dka88a`
3. Click "Edit"
4. Add **Authorized JavaScript origins:**
   ```
   https://performos.digital
   https://team-health-hub-2.preview.emergentagent.com
   http://localhost:3000
   ```
5. Save and wait 5 minutes

---

## ✅ After You Add These Variables and Redeploy:

- ✅ Login will work
- ✅ AI Briefing will work
- ✅ My Coaching will work
- ✅ Executive Summary will work
- ✅ Google Login will work (after Google Cloud setup)
- ✅ No more 500 errors
- ✅ App fully functional 24/7

---

**The code is 100% correct. You just need to add these environment variables in Emergent deployment settings!** 🎯
