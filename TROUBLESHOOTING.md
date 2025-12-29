# 🔧 Troubleshooting Guide for Railway Deployment

This guide covers common issues you might encounter when deploying AutoKPI to Railway.app and how to fix them.

## 🚨 Build Failures

### Issue: Build fails with "No matching distribution found"

**Symptoms:**
- Build logs show: `ERROR: Could not find a version that satisfies the requirement`
- Build fails during pip install

**Solutions:**
1. **Check requirements.txt format**: Ensure you're using `>=` instead of `==` for version pinning
2. **Check package names**: Verify all package names are spelled correctly
3. **Check Python version**: Railway auto-detects Python version. Ensure packages are compatible
4. **Update requirements.txt**: Use more flexible version constraints

**Example fix:**
```txt
# ❌ Bad (too specific)
pandas==2.0.0

# ✅ Good (flexible)
pandas>=2.0.0
```

### Issue: Build fails with "Command failed" or "Build timeout"

**Symptoms:**
- Build process hangs or fails without clear error
- Takes too long to install packages

**Solutions:**
1. **Check for heavy dependencies**: Remove unnecessary packages
2. **Optimize requirements.txt**: Only include packages actually used
3. **Check Railway logs**: Look for specific package causing issues
4. **Try building locally**: Reproduce the issue locally to debug

### Issue: Missing dependencies after deployment

**Symptoms:**
- App builds successfully but crashes at runtime
- Import errors in logs: `ModuleNotFoundError: No module named 'X'`

**Solutions:**
1. **Check all imports**: Go through your code and list all imported packages
2. **Add missing packages**: Add any missing packages to `requirements.txt`
3. **Check sub-dependencies**: Some packages have dependencies that need to be explicit
4. **Test locally**: Run `pip install -r requirements.txt` locally and check for warnings

**Common missing packages:**
- `python-dotenv` (if using `.env` files)
- `openai` (if using LLM features, even if optional)
- `openpyxl` (for Excel file support)

## 🌐 Runtime Errors

### Issue: App crashes with "Port already in use" or "Address already in use"

**Symptoms:**
- App fails to start
- Logs show port-related errors

**Solutions:**
1. **Check start command**: Must use `$PORT` environment variable:
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
2. **Verify address**: Must use `0.0.0.0` not `localhost` or `127.0.0.1`
3. **Remove hardcoded ports**: Don't hardcode port numbers in code

### Issue: App shows "Application Error" or "Cannot connect"

**Symptoms:**
- Domain shows error page
- App doesn't load

**Solutions:**
1. **Check deployment status**: Go to Railway dashboard → Deployments
2. **Check logs**: Look for errors in deployment logs
3. **Verify start command**: Check Settings → Start Command is correct
4. **Check if app is sleeping**: Free tier apps sleep after 7 days - wait 10-30 seconds

### Issue: App loads but shows blank page or errors

**Symptoms:**
- App domain loads but shows errors
- Streamlit shows error messages

**Solutions:**
1. **Check Railway logs**: View runtime logs for Python errors
2. **Check browser console**: Look for JavaScript errors
3. **Verify all imports**: Check that all Python imports work
4. **Check file paths**: Ensure file paths work in production environment

### Issue: File upload doesn't work

**Symptoms:**
- File uploader appears but files don't process
- Errors when trying to upload files

**Solutions:**
1. **Check file size limits**: Railway has file size limits
2. **Check Streamlit config**: Verify Streamlit configuration is correct
3. **Check error logs**: Look for specific upload errors in logs
4. **Test with smaller files**: Try with smaller CSV files first

## 💾 Memory Issues

### Issue: App crashes with "Memory limit exceeded" or "Out of memory"

**Symptoms:**
- App crashes when processing large datasets
- Deployment fails due to memory

**Solutions:**
1. **Optimize data processing**: Process data in chunks, not all at once
2. **Limit dataset size**: Add file size limits in your app
3. **Upgrade Railway plan**: Free tier has memory limits
4. **Check memory usage**: Monitor memory in Railway dashboard

### Issue: Slow performance or timeouts

**Symptoms:**
- App is very slow
- Requests timeout

**Solutions:**
1. **Optimize code**: Profile your code to find bottlenecks
2. **Limit dataset size**: Don't process entire large files at once
3. **Add caching**: Use Streamlit's caching features
4. **Check Railway resources**: Verify you're not hitting resource limits

## 🔑 Environment Variables

### Issue: Environment variables not working

**Symptoms:**
- App can't access environment variables
- API keys not found

**Solutions:**
1. **Check Railway Variables**: Go to Variables tab and verify variables are set
2. **Check variable names**: Ensure names match exactly (case-sensitive)
3. **Restart service**: Redeploy after adding/changing variables
4. **Check code**: Verify code reads from `os.getenv()` correctly

**Example:**
```python
# ✅ Correct
api_key = os.getenv('OPENAI_API_KEY')

# ❌ Wrong (hardcoded)
api_key = 'your_key_here'
```

## 🌍 Domain & Network Issues

### Issue: Domain not working or shows 404

**Symptoms:**
- Domain URL shows 404 or error
- App not accessible

**Solutions:**
1. **Verify domain generation**: Check Settings → Domains that domain is generated
2. **Wait for DNS propagation**: Can take a few minutes
3. **Check deployment status**: Ensure latest deployment succeeded
4. **Try direct Railway URL**: Use the Railway-provided URL instead

### Issue: App is sleeping (free tier behavior)

**Symptoms:**
- App takes 10-30 seconds to load
- First request is slow

**Solutions:**
1. **This is normal**: Free tier apps sleep after 7 days of inactivity
2. **Be patient**: Wait 10-30 seconds for app to wake up
3. **Don't create keep-alive scripts**: Violates Railway terms of service
4. **Expect wake-up delay**: This is expected behavior for free tier

## 📦 Dependency Issues

### Issue: Version conflicts between packages

**Symptoms:**
- Build succeeds but runtime errors occur
- Package compatibility issues

**Solutions:**
1. **Use flexible versions**: Use `>=` instead of `==` in requirements.txt
2. **Update packages**: Try updating to newer versions
3. **Check compatibility**: Verify package versions are compatible
4. **Test locally**: Reproduce locally to identify conflicts

**Example:**
```txt
# ❌ Bad (can cause conflicts)
pandas==2.0.0
numpy==1.24.0

# ✅ Good (flexible)
pandas>=2.0.0
numpy>=1.24.0
```

### Issue: Import errors for optional dependencies

**Symptoms:**
- Errors like "No module named 'openai'" even though it's optional

**Solutions:**
1. **Add to requirements.txt**: Even optional packages should be listed if imported
2. **Use try/except**: Code should handle ImportError gracefully:
   ```python
   try:
       from openai import OpenAI
       OPENAI_AVAILABLE = True
   except ImportError:
       OPENAI_AVAILABLE = False
   ```
3. **Check conditional imports**: Verify optional features check availability

## 🔄 Deployment Issues

### Issue: Auto-deployment not working

**Symptoms:**
- Pushing to GitHub doesn't trigger deployment
- Manual deployment needed

**Solutions:**
1. **Check GitHub connection**: Verify Railway is connected to correct repo
2. **Check branch**: Ensure Railway watches correct branch (main/master)
3. **Check permissions**: Verify Railway has access to repository
4. **Manual trigger**: Try triggering deployment manually in Railway

### Issue: Deployment succeeds but app doesn't update

**Symptoms:**
- New deployment shows success but changes aren't visible
- Old version still running

**Solutions:**
1. **Clear browser cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
2. **Check deployment**: Verify correct deployment is active
3. **Wait a few minutes**: Sometimes takes time to propagate
4. **Check logs**: Verify new code is actually running

## 🐍 Python-Specific Issues

### Issue: Python version mismatch

**Symptoms:**
- Build fails or app crashes
- Syntax errors in logs

**Solutions:**
1. **Railway auto-detects**: Railway usually detects Python version correctly
2. **Check Python version**: Ensure code is compatible with Python 3.8+
3. **Specify version** (if needed): Add `runtime.txt` with Python version:
   ```
   python-3.11
   ```

### Issue: Missing system dependencies

**Symptoms:**
- Packages fail to install
- Native extensions don't compile

**Solutions:**
1. **Check package requirements**: Some packages need system libraries
2. **Railway handles most**: Railway usually provides common system libraries
3. **Contact support**: For uncommon system dependencies, contact Railway support

## 📝 Log Analysis

### How to Read Railway Logs

1. **Access logs**: Railway dashboard → Your service → Deployments → Click deployment → View Logs
2. **Build logs**: Shows pip install output and build process
3. **Runtime logs**: Shows application output and errors
4. **Look for keywords**: ERROR, WARNING, Traceback, Exception

### Common Log Patterns

**Successful build:**
```
Installing collected packages: ...
Successfully installed ...
```

**Failed build:**
```
ERROR: Could not find a version...
ERROR: Command failed...
```

**Successful start:**
```
You can now view your Streamlit app in your browser.
```

**Failed start:**
```
Traceback (most recent call last):
...
ModuleNotFoundError: ...
```

## 🆘 Getting More Help

### When to Check Logs

- ✅ **First step**: Always check Railway logs first
- ✅ **Build failures**: Check build logs
- ✅ **Runtime errors**: Check runtime logs
- ✅ **Deployment issues**: Check deployment logs

### When to Check Code

- ✅ **Import errors**: Check all imports in code
- ✅ **Path issues**: Check file paths
- ✅ **Configuration**: Check Streamlit config
- ✅ **Dependencies**: Verify requirements.txt

### Additional Resources

1. **Railway Documentation**: https://docs.railway.app
2. **Streamlit Documentation**: https://docs.streamlit.io
3. **Railway Community**: Railway Discord/Forum
4. **GitHub Issues**: Open an issue in your repo

### Before Asking for Help

1. ✅ Checked Railway logs
2. ✅ Checked browser console
3. ✅ Verified requirements.txt
4. ✅ Tested locally
5. ✅ Searched Railway documentation
6. ✅ Checked this troubleshooting guide

## ✅ Quick Fix Checklist

For common issues, try these in order:

1. **Check start command**: Must be `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
2. **Check requirements.txt**: All dependencies listed with `>=`
3. **Check logs**: Look for specific error messages
4. **Verify deployment**: Check deployment status in Railway
5. **Test locally**: Ensure app works locally first
6. **Clear cache**: Hard refresh browser
7. **Wait for wake-up**: If free tier, wait 10-30 seconds

---

**Remember**: Most issues are related to:
- ❌ Wrong start command (most common!)
- ❌ Missing dependencies in requirements.txt
- ❌ Port/address configuration
- ❌ Environment variables not set
- ⏰ App sleeping (normal for free tier)

Check these first before digging deeper! 🚀

