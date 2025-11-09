# 🚀 Quick Deploy Guide - AutoKPI

## Fastest Way: Streamlit Cloud (5 minutes!)

### Step 1: Push to GitHub
```bash
cd /Users/anithalakshmipathy/Documents/AutoKPI
git init
git add .
git commit -m "AutoKPI - AI-Powered Analytics Toolkit"
git remote add origin https://github.com/YOUR_USERNAME/AutoKPI.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to **https://share.streamlit.io**
2. Click **"Sign in"** → Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/AutoKPI`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy"**

### Step 3: Done! 🎉
Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

---

## Alternative: Heroku (10 minutes)

```bash
# Install Heroku CLI (if not installed)
# macOS: brew install heroku

# Login
heroku login

# Create app
heroku create autokpi-yourname

# Deploy
git init
git add .
git commit -m "Deploy AutoKPI"
git push heroku main

# Open
heroku open
```

---

## What's Included

✅ All dependencies in `requirements.txt`
✅ Dark theme configuration
✅ Production-ready settings
✅ No LLM API keys required
✅ Ready to deploy!

---

## Your App Features

- 📊 Automatic KPI generation
- 🎨 Beautiful dark theme UI
- 📈 Interactive visualizations
- 💾 Multiple export formats
- 🔍 Advanced analytics
- 📖 Detailed chart explanations

---

**Need help? Check `DEPLOY.md` for detailed instructions!**

