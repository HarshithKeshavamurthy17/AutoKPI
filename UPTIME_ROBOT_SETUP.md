# 🔄 Keep AutoKPI Live with Uptime Robot

## Why Use Uptime Robot?

Streamlit Cloud free tier may put your app to sleep after inactivity. Uptime Robot will ping your app every 5 minutes to keep it awake!

## 🚀 Setup Instructions

### Step 1: Get Your Streamlit App URL

After deploying on Streamlit Cloud, you'll get a URL like:
- `https://autokpi.streamlit.app`
- Or `https://YOUR_APP_NAME.streamlit.app`

### Step 2: Sign Up for Uptime Robot

1. **Visit**: https://uptimerobot.com
2. **Click**: "Sign Up" (Free plan is perfect!)
3. **Create account** with email or Google/GitHub

### Step 3: Add New Monitor

1. **Click**: "Add New Monitor" button
2. **Monitor Type**: Select **"HTTP(s)"**
3. **Friendly Name**: `AutoKPI - Keep Alive`
4. **URL**: 
   ```
   https://YOUR_APP_NAME.streamlit.app/_stcore/health
   ```
   Replace `YOUR_APP_NAME` with your actual Streamlit app name
   
   **Example**: `https://autokpi.streamlit.app/_stcore/health`

5. **Monitoring Interval**: Select **"Every 5 minutes"**
6. **Alert Contacts**: Add your email (optional)
7. **Click**: "Create Monitor"

### Step 4: Done! 🎉

Uptime Robot will now ping your app every 5 minutes, keeping it awake 24/7!

---

## 📊 Alternative: Ping Main Page

If the health endpoint doesn't work, you can also ping the main page:

**URL**: `https://YOUR_APP_NAME.streamlit.app`

This will load the full app, which also keeps it alive.

---

## 🔧 Other Options

### Option 1: Cron-Job.org (Free)
1. Visit: https://cron-job.org
2. Create account
3. Add new cron job:
   - URL: `https://YOUR_APP_NAME.streamlit.app/_stcore/health`
   - Schedule: Every 5 minutes
   - Method: GET

### Option 2: EasyCron (Free Tier)
1. Visit: https://www.easycron.com
2. Sign up for free account
3. Create cron job to ping your URL every 5 minutes

### Option 3: Python Script (Local)
If you want to run it from your computer:

```python
import requests
import time
from datetime import datetime

URL = "https://YOUR_APP_NAME.streamlit.app/_stcore/health"

while True:
    try:
        response = requests.get(URL, timeout=10)
        print(f"{datetime.now()}: ✅ Pinged - Status {response.status_code}")
    except Exception as e:
        print(f"{datetime.now()}: ❌ Error - {e}")
    time.sleep(300)  # 5 minutes = 300 seconds
```

---

## 📝 Quick Setup Checklist

- [ ] Deploy app on Streamlit Cloud
- [ ] Get your app URL
- [ ] Sign up for Uptime Robot (free)
- [ ] Add monitor with health endpoint URL
- [ ] Set interval to 5 minutes
- [ ] Verify monitor is active
- [ ] App stays awake! 🎉

---

## 🎯 Recommended Settings

**Monitor Type**: HTTP(s)  
**URL**: `https://YOUR_APP_NAME.streamlit.app/_stcore/health`  
**Interval**: Every 5 minutes  
**Timeout**: 30 seconds  
**Status**: Enabled  

---

## ✅ Verify It's Working

1. Check Uptime Robot dashboard - should show "UP" status
2. Visit your app URL - should load instantly (not sleeping)
3. Check monitoring logs - should show successful pings every 5 minutes

---

## 🆘 Troubleshooting

**If health endpoint doesn't work:**
- Try pinging the main page: `https://YOUR_APP_NAME.streamlit.app`
- Make sure your app is deployed and accessible
- Check that the URL is correct

**If app still goes to sleep:**
- Reduce interval to 3 minutes
- Use main page URL instead of health endpoint
- Check Uptime Robot logs for errors

---

## 💡 Pro Tips

1. **Free Plan**: Uptime Robot free plan allows 50 monitors - perfect for one app!
2. **Notifications**: Set up email alerts if your app goes down
3. **Multiple Services**: You can use multiple services for redundancy
4. **Monitor Dashboard**: Check Uptime Robot dashboard to see uptime stats

---

## 🎊 You're All Set!

Your AutoKPI will now stay awake 24/7, ready to analyze datasets anytime! 🚀



