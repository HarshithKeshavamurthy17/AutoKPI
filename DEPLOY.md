# 🚀 Deploy AutoKPI to Production

## Option 1: Streamlit Cloud (Easiest - Recommended)

### Steps:
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - AutoKPI"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/AutoKPI.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/AutoKPI`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://YOUR_APP_NAME.streamlit.app`

---

## Option 2: Heroku

### Steps:
1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create autokpi-yourname
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy AutoKPI"
   git push heroku main
   ```

5. **Open your app**
   ```bash
   heroku open
   ```

---

## Option 3: Railway

### Steps:
1. **Go to Railway**: https://railway.app
2. **Sign in with GitHub**
3. **New Project** → **Deploy from GitHub repo**
4. **Select your AutoKPI repository**
5. **Railway will auto-detect Streamlit and deploy**

---

## Option 4: Docker (Any Platform)

### Create Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run:
```bash
docker build -t autokpi .
docker run -p 8501:8501 autokpi
```

---

## Option 5: AWS/Azure/GCP

### For AWS EC2:
1. Launch EC2 instance (Ubuntu)
2. Install Python 3.12
3. Clone repository
4. Install dependencies
5. Run: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
6. Configure security group to allow port 8501

### For Google Cloud Run:
```bash
gcloud run deploy autokpi --source . --platform managed --region us-central1
```

---

## Environment Variables (Optional)

If you need to set environment variables:
- **Streamlit Cloud**: Settings → Secrets
- **Heroku**: `heroku config:set KEY=value`
- **Railway**: Variables tab

---

## Quick Deploy Checklist

- [ ] Code is pushed to GitHub
- [ ] `requirements.txt` is up to date
- [ ] `Procfile` exists (for Heroku)
- [ ] `.streamlit/config.toml` is configured
- [ ] Tested locally
- [ ] Deployed to chosen platform
- [ ] App is accessible and working

---

## Need Help?

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Heroku Docs**: https://devcenter.heroku.com/articles/getting-started-with-python
- **Railway Docs**: https://docs.railway.app

---

## 🎉 Once Deployed!

Your AutoKPI will be live and ready to analyze datasets from anywhere in the world!

