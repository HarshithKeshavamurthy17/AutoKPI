# 🚂 Railway.app Deployment Guide for AutoKPI

This guide will walk you through deploying your AutoKPI Streamlit application to Railway.app.

## 📋 Prerequisites

- A GitHub account
- Your AutoKPI project pushed to a GitHub repository
- A Railway.app account (free tier provides $5 monthly credit)

## 🚀 Step-by-Step Deployment

### Step 1: Sign Up for Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"Start a New Project"** or **"Login"** if you already have an account
3. Sign up using your GitHub account (recommended for easier integration)

### Step 2: Create a New Project

1. Once logged in, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub repositories if prompted
4. Select your **AutoKPI** repository from the list

### Step 3: Configure the Deployment

Railway will automatically detect that this is a Python project and start building. 

**Option A: Using Procfile (Recommended - Already Configured!)**

Your project already includes a `Procfile` with the correct configuration:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Railway will automatically use this Procfile, so you don't need to set the start command manually! ✅

**Option B: Manual Start Command (Alternative)**

If you prefer to set it manually:

1. Click on your newly created service
2. Go to the **"Settings"** tab
3. Scroll down to **"Start Command"**
4. Set the start command to:
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
5. Click **"Save"**

**Note**: Since you have a Procfile, Railway will use it automatically. You can skip this step if the Procfile is present and correct.

### Step 4: Verify Build Configuration

1. In the **"Settings"** tab, check that:
   - **Build Command**: (Leave empty - Railway auto-detects Python projects)
   - **Root Directory**: (Leave empty unless your app is in a subdirectory)
   - **Healthcheck Path**: (Leave empty for Streamlit apps)

### Step 5: Set Environment Variables (Optional)

If you want to use LLM features with OpenAI:

1. Go to the **"Variables"** tab
2. Click **"New Variable"**
3. Add:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
4. Click **"Add"**

**Note**: LLM features are optional. The app works perfectly without this variable.

### Step 6: Generate a Domain

1. Go to the **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Railway will create a domain like: `autokpi-production.up.railway.app`
5. Copy the domain URL - this is your live app URL!

### Step 7: Wait for Deployment

1. Go to the **"Deployments"** tab
2. Watch the build logs in real-time
3. Wait for the deployment to complete (usually 2-5 minutes)
4. Once you see "Deploy Succeeded", your app is live!

### Step 8: Test Your Deployment

1. Click on the generated domain to open your app
2. Test uploading a dataset
3. Verify all features work correctly
4. Check that charts and visualizations render properly

## ✅ Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can upload CSV/Excel files
- [ ] Schema inference works
- [ ] KPI generation works
- [ ] Charts render correctly
- [ ] Export functions work
- [ ] No errors in Railway logs

## 🔄 Auto-Deployment

Railway automatically deploys whenever you push to your main/master branch on GitHub. This means:

- **No manual redeployments needed** - Just push to GitHub and Railway handles the rest
- Deployment happens automatically in 2-5 minutes
- You can see deployment status in the Railway dashboard

## 🌐 Custom Domain (Optional)

If you want to use a custom domain:

1. Go to **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Add your domain name
4. Follow Railway's DNS configuration instructions
5. Wait for DNS propagation (can take up to 48 hours)

## 📊 Monitoring Your App

### View Logs

1. Go to your service in Railway dashboard
2. Click on the **"Deployments"** tab
3. Click on any deployment to see logs
4. Use **"View Logs"** button for real-time logs

### Check Deployment Status

- Green checkmark = Successful deployment
- Red X = Failed deployment (check logs for errors)
- Yellow/yellow circle = In progress

## 💰 Free Tier Information

Railway's free tier includes:

- **$5 monthly credit** (enough for small apps)
- **Sleep mode after 7 days** of inactivity (apps wake up automatically on next request)
- **No credit card required** for free tier
- **Automatic wake-up** - Apps wake up within 10-30 seconds when accessed

### Important Notes about Free Tier:

- ⏰ **Sleep Mode**: Your app will sleep after 7 days of inactivity (this is normal and expected)
- 🔄 **Wake-up Time**: First request after sleep may take 10-30 seconds (be patient)
- 💤 **No Keep-Alive Scripts**: Don't create scripts to ping your app constantly (violates terms of service)
- ✅ **Normal Behavior**: Sleep/wake cycle is expected for free tier hosting

## 🛠️ Common Configuration Issues

### Port Configuration

Make sure your start command uses `$PORT` environment variable:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### Missing Dependencies

If the build fails due to missing packages:
1. Check that all dependencies are in `requirements.txt`
2. Ensure all imports are covered
3. Check the build logs for specific missing packages

### Memory Issues

If your app crashes due to memory:
1. Check Railway logs for memory errors
2. Consider optimizing your code for large datasets
3. Railway free tier has memory limits - upgrade if needed

## 🔧 Updating Your App

To update your deployed app:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. Railway automatically detects the push and starts a new deployment
4. Wait 2-5 minutes for deployment to complete
5. Your app is updated!

## 📝 Tips for Success

1. **Test Locally First**: Always test your app locally before pushing to GitHub
2. **Check Logs**: If something goes wrong, check Railway logs first
3. **Version Pinning**: Use `>=` in requirements.txt for flexibility (already done!)
4. **Environment Variables**: Keep sensitive data in Railway variables, not in code
5. **Monitor Usage**: Check your Railway dashboard for credit usage

## 🆘 Need Help?

If you encounter issues:

1. Check the **Troubleshooting Guide** (`TROUBLESHOOTING.md`)
2. Review Railway logs in the dashboard
3. Check Railway's [documentation](https://docs.railway.app)
4. Open an issue on GitHub

## 🎉 Success!

Once deployed, your AutoKPI app will be live at your Railway domain URL. Share it with the world!

**Example URL Format**: `https://autokpi-production.up.railway.app`

---

**Next Steps**:
- Update your README.md with the live URL
- Share your app with others
- Monitor usage and performance
- Enjoy your deployed app! 🚀

