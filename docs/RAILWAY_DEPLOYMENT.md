# Railway Deployment Guide for Golden Minutes

## 🚀 Deploy to Railway (Free Forever)

### Prerequisites
- GitHub account
- Git installed

### Step 1: Prepare Your Project

#### 1.1 Create `requirements.txt`
```bash
cd "d:\Golden Minutes"
pip freeze > requirements.txt
```

#### 1.2 Create `runtime.txt`
```
python-3.10.0
```

#### 1.3 Create `Procfile`
```
web: gunicorn golden_minutes.wsgi --log-file -
```

#### 1.4 Install Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

#### 1.5 Update `settings.py`

Add to the end of `golden_minutes/settings.py`:

```python
# Railway Deployment Settings
import os

# Allow Railway domain
ALLOWED_HOSTS = ['*']  # Railway will set proper host

# Database (Railway provides PostgreSQL)
import dj_database_url
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }

# Static files (Railway)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Security for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

#### 1.6 Install dj-database-url
```bash
pip install dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

---

### Step 2: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Railway deployment"

# Create GitHub repo (go to github.com/new)
# Then connect:
git remote add origin https://github.com/YOUR_USERNAME/golden-minutes.git
git branch -M main
git push -u origin main
```

---

### Step 3: Deploy to Railway

1. **Go to https://railway.app**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose `golden-minutes`**
6. **Railway auto-detects Django!**

Railway will:
- ✅ Install dependencies
- ✅ Run migrations
- ✅ Start server
- ✅ Give you HTTPS URL

---

### Step 4: Add PostgreSQL Database

1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically connects it!

---

### Step 5: Set Environment Variables

In Railway dashboard:
1. Click on your service
2. Go to "Variables"
3. Add:
   - `DJANGO_SECRET_KEY`: (generate new one)
   - `DEBUG`: `False`

---

### Step 6: Get Your URL

Railway gives you:
```
https://golden-minutes-production.up.railway.app
```

**This URL:**
- ✅ Works 24/7
- ✅ Has HTTPS (required for PWA)
- ✅ Auto-updates when you push to GitHub
- ✅ Free forever (500 hours/month)

---

### Step 7: Test PWA Installation

1. **Open URL on Android Chrome**
2. **Chrome shows "Install" button**
3. **Tap "Add to Home Screen"**
4. **App appears on home screen!**

---

## 🔧 Troubleshooting

### Issue: "Application Error"
**Solution:** Check Railway logs:
1. Click on your service
2. Go to "Deployments"
3. Click latest deployment
4. View logs

### Issue: Static files not loading
**Solution:** Run collectstatic:
```bash
python manage.py collectstatic --noinput
```
Add to Procfile:
```
release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn golden_minutes.wsgi --log-file -
```

### Issue: Database error
**Solution:** Railway auto-creates PostgreSQL. Just add it from dashboard.

---

## 📱 After Deployment

Your app will be available at:
```
https://your-app-name.up.railway.app
```

Users can:
1. Visit URL on Android
2. Install as PWA
3. Use like native app
4. Get push notifications
5. Use offline (service worker)

---

## 🎯 Next Steps

1. **Deploy to Railway** (follow steps above)
2. **Test on Android phone**
3. **Share URL with users**
4. **They install as PWA**
5. **App works 24/7!**

---

## 💰 Cost

**Railway Free Tier:**
- 500 hours/month
- $5 credit/month
- PostgreSQL included
- HTTPS included
- **Perfect for your app!**

If you exceed free tier:
- ~$5-10/month for small apps
- Pay only for what you use

---

## 🚀 Ready to Deploy?

Run these commands:

```bash
# 1. Install dependencies
pip install gunicorn dj-database-url psycopg2-binary

# 2. Update requirements
pip freeze > requirements.txt

# 3. Commit changes
git add .
git commit -m "Ready for Railway"
git push

# 4. Go to railway.app and deploy!
```

**Want me to help you with any of these steps?**
