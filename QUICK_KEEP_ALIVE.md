# ⚡ Quick Keep-Alive Setup

## 🎯 Fastest Method: Uptime Robot (Recommended)

### 1. Sign Up (Free)
- Go to: **https://uptimerobot.com**
- Click "Sign Up (Free)
- Sign up with email or GitHub

### 2. Add Monitor
- Click **"Add New Monitor"**
- **Type**: HTTP(s)
- **Name**: `AutoKPI Keep Alive`
- **URL**: `https://YOUR_APP_NAME.streamlit.app/_stcore/health`
  - Replace `YOUR_APP_NAME` with your actual app name
- **Interval**: Every 5 minutes
- Click **"Create Monitor"**

### 3. Done! ✅
Your app will stay awake 24/7!

---

## 📋 Your App URL Format

After deploying on Streamlit Cloud, your URL will be:
- `https://autokpi.streamlit.app` (if you named it "autokpi")
- Or `https://YOUR_CUSTOM_NAME.streamlit.app`

**Health Check URL**: `https://YOUR_APP_NAME.streamlit.app/_stcore/health`

---

## 🔄 Alternative: Cron-Job.org

1. Visit: **https://cron-job.org**
2. Sign up (free)
3. Create cron job:
   - URL: `https://YOUR_APP_NAME.streamlit.app/_stcore/health`
   - Schedule: `*/5 * * * *` (every 5 minutes)
   - Method: GET

---

## 💻 Local Script (Optional)

If you want to run a script from your computer:

1. Update `keep_alive.py` with your app URL
2. Install: `pip install requests`
3. Run: `python3 keep_alive.py`

This will ping your app every 5 minutes from your computer.

---

## ✅ Verify It Works

1. Check Uptime Robot dashboard → Should show "UP"
2. Visit your app → Should load instantly (not sleeping)
3. Wait 5 minutes → Check logs show successful pings

---

## 🎊 That's It!

Your AutoKPI will now stay awake and ready to use anytime! 🚀

