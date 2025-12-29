# ✅ Railway Deployment Checklist for AutoKPI

Use this checklist to ensure a successful deployment to Railway.app.

## 📋 Pre-Deployment Checklist

### Code Preparation
- [ ] All code is committed and pushed to GitHub
- [ ] `requirements.txt` exists and uses `>=` (not `==`) for version pinning
- [ ] All dependencies are listed in `requirements.txt`:
  - [ ] streamlit
  - [ ] pandas
  - [ ] numpy
  - [ ] altair
  - [ ] openpyxl
  - [ ] scipy
  - [ ] plotly
  - [ ] python-dotenv
  - [ ] openai (optional, for LLM features)
- [ ] Main application file exists (`app.py`)
- [ ] All imports work correctly (test locally)
- [ ] No hardcoded file paths that won't work in production
- [ ] No hardcoded ports or addresses

### Local Testing
- [ ] App runs successfully locally: `streamlit run app.py`
- [ ] Can upload CSV/Excel files
- [ ] Schema inference works
- [ ] KPI generation works
- [ ] Charts render correctly
- [ ] Export functions work
- [ ] No console errors

### GitHub Repository
- [ ] Repository is public or Railway has access to private repo
- [ ] Repository contains all necessary files
- [ ] `.gitignore` excludes unnecessary files (but includes required ones)
- [ ] README.md is up to date

## 🚂 Railway Setup Checklist

### Account & Project Setup
- [ ] Created Railway account at [railway.app](https://railway.app)
- [ ] Connected GitHub account to Railway
- [ ] Created new project
- [ ] Selected AutoKPI repository for deployment

### Configuration
- [ ] Start command is set: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- [ ] Build command is empty (Railway auto-detects Python)
- [ ] Root directory is empty (unless app is in subdirectory)
- [ ] Python version is compatible (Railway auto-detects)

### Environment Variables (Optional)
- [ ] `OPENAI_API_KEY` added if using LLM features (optional)
- [ ] All required environment variables are set

### Domain Setup
- [ ] Generated Railway domain (e.g., `autokpi-production.up.railway.app`)
- [ ] Domain URL copied and saved

## 🚀 Deployment Process

### Initial Deployment
- [ ] Build started automatically after connecting repo
- [ ] Build logs show successful package installation
- [ ] No build errors in logs
- [ ] Deployment status shows "Succeeded"
- [ ] App is accessible via generated domain

### Post-Deployment Testing
- [ ] App loads successfully (wait 10-30 seconds if just woke up)
- [ ] Can upload CSV file
- [ ] Can upload Excel file
- [ ] Schema inference displays correctly
- [ ] "Generate KPIs" button works
- [ ] KPIs are generated and displayed
- [ ] Charts render correctly (bar, line, histogram, etc.)
- [ ] Chart explanations are displayed
- [ ] Export to JSON works
- [ ] Export to Markdown works
- [ ] Export to Dashboard Spec works
- [ ] No JavaScript errors in browser console
- [ ] No errors in Railway logs

### Functionality Verification
- [ ] Data quality assessment works
- [ ] Advanced analytics (correlations, outliers) work
- [ ] Creative KPIs are generated
- [ ] Auto insights are displayed
- [ ] Example datasets can be loaded (if applicable)
- [ ] All UI elements are visible and functional
- [ ] Dark theme renders correctly
- [ ] Responsive design works on different screen sizes

## 🔄 Continuous Deployment

### Auto-Deployment Setup
- [ ] Confirmed Railway is connected to correct GitHub repo
- [ ] Confirmed Railway watches correct branch (usually `main` or `master`)
- [ ] Tested auto-deployment by making a small change and pushing

### Update Process
- [ ] Made code changes locally
- [ ] Tested changes locally
- [ ] Committed changes: `git commit -m "Description"`
- [ ] Pushed to GitHub: `git push`
- [ ] Railway automatically started new deployment
- [ ] New deployment completed successfully
- [ ] Verified changes are live on deployed app

## 📊 Monitoring & Maintenance

### Regular Checks
- [ ] Check Railway dashboard for deployment status
- [ ] Review logs for any warnings or errors
- [ ] Monitor credit usage (free tier: $5/month)
- [ ] Test app functionality periodically
- [ ] Verify app wakes up correctly after sleep period

### Log Monitoring
- [ ] Know how to access Railway logs
- [ ] Understand how to interpret build logs
- [ ] Know how to view runtime logs
- [ ] Check logs when app has issues

### Performance
- [ ] App loads within reasonable time (10-30 seconds after wake)
- [ ] No memory errors in logs
- [ ] No timeout errors
- [ ] File uploads work correctly
- [ ] Processing completes without errors

## 🐛 Troubleshooting Preparation

### Know Where to Look
- [ ] Railway dashboard → Deployments tab for build logs
- [ ] Railway dashboard → Logs for runtime logs
- [ ] Browser console for frontend errors
- [ ] Railway settings for configuration issues

### Common Issues to Watch For
- [ ] Build failures (check requirements.txt)
- [ ] Port configuration errors
- [ ] Missing dependencies
- [ ] Environment variable issues
- [ ] Memory limits exceeded
- [ ] Timeout errors

## 📝 Documentation

### Update Documentation
- [ ] README.md includes Railway deployment info
- [ ] README.md includes live demo URL
- [ ] README.md includes free tier wake-up note
- [ ] RAILWAY_DEPLOY.md guide is complete
- [ ] TROUBLESHOOTING.md guide is available

## ✅ Final Verification

### Everything Works
- [ ] All checklist items completed
- [ ] App is live and accessible
- [ ] All features tested and working
- [ ] Documentation is updated
- [ ] Ready to share with users!

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ App is accessible via Railway domain
- ✅ All core features work correctly
- ✅ No critical errors in logs
- ✅ App wakes up correctly after sleep
- ✅ Auto-deployment works for updates
- ✅ Documentation is complete

---

**Next Steps After Successful Deployment:**
1. Share your live app URL
2. Update portfolio/README with live demo link
3. Monitor usage and performance
4. Enjoy your deployed app! 🚀

---

**Need Help?**
- Check [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed deployment steps
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and fixes
- Review Railway logs for specific errors
- Check Railway documentation: https://docs.railway.app

