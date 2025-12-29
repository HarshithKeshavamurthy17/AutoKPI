# ⚡ Railway Quick Start Guide

**TL;DR**: Deploy AutoKPI to Railway in 5 minutes!

## 🚀 Quick Deploy Steps

1. **Push to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push
   ```

2. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Sign up with GitHub

3. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your AutoKPI repository
   - Railway will automatically use your `Procfile` (already configured!) ✅

4. **Generate Domain** (Optional - Railway will auto-generate one)
   - Go to Settings → Domains
   - Click "Generate Domain" (if not already generated)
   - Copy your URL (e.g., `autokpi-production.up.railway.app`)

5. **Done!** 🎉
   - Wait 2-5 minutes for deployment
   - Visit your domain URL
   - Your app is live!

## ⚙️ Optional: Environment Variables

Only needed if using LLM features:

1. Go to Variables tab
2. Add: `OPENAI_API_KEY` = `your_key_here`
3. Save

## 📝 What You Need

- ✅ GitHub repository with your code
- ✅ `requirements.txt` (already included!)
- ✅ `app.py` as main file (already included!)
- ✅ Railway account (free tier is fine!)

## 🔄 Auto-Deployment

Railway automatically deploys when you push to GitHub. Just:
```bash
git push
```
And Railway handles the rest!

## ⏰ Free Tier Notes

- App sleeps after 7 days of inactivity (normal!)
- First visit after sleep takes 10-30 seconds (be patient!)
- $5 monthly credit included (usually enough for small apps)

## 🆘 Problems?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed guide
- Check Railway logs in dashboard

## ✅ Verification

After deployment, test:
- [ ] App loads at your Railway URL
- [ ] Can upload CSV/Excel files
- [ ] KPIs generate correctly
- [ ] Charts render properly

---

**That's it!** Your app should be live in ~5 minutes. 🚂🚀

