# 🗺️ Mapbox Setup Guide

## Get Your Free Mapbox Token

### Step 1: Create Account
1. Go to: **https://account.mapbox.com/auth/signup/**
2. Sign up with your email (no credit card required)
3. Verify your email

### Step 2: Get Your Token
1. After logging in, you'll see your **Default public token**
2. It looks like: `pk.eyJ1Ijoi...` (starts with `pk.`)
3. Copy this token

### Step 3: Add Token to Django
1. Open: `d:\Golden Minutes\golden_minutes\settings.py`
2. Find the line:
   ```python
   MAPBOX_ACCESS_TOKEN = 'YOUR_MAPBOX_TOKEN_HERE'
   ```
3. Replace `'YOUR_MAPBOX_TOKEN_HERE'` with your actual token:
   ```python
   MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoieW91cnVzZXJuYW1lIiwiYSI6ImNsZjR5...'
   ```

### Step 4: Restart Server
```bash
# Stop the server (Ctrl+C)
# Start it again
python manage.py runserver
```

### Step 5: Enjoy!
Visit: **http://127.0.0.1:8000/emergencies/map/**

You'll now see:
- ✅ Beautiful Mapbox streets view
- ✅ 3D tilted perspective
- ✅ 3 map styles (Streets, Satellite, Dark)
- ✅ Smooth animations
- ✅ Professional design

## 🎨 Map Features

### Map Styles
- **Streets** - Default clean street view
- **Satellite** - Aerial imagery with labels
- **Dark** - Dark mode for night viewing

### Interactive Elements
- **Zoom** - Mouse wheel or +/- buttons
- **Rotate** - Right-click + drag
- **Tilt** - Ctrl + drag
- **Fullscreen** - Click fullscreen button

### Emergency Features
- **Green Marker** - Your location (if volunteer)
- **Red Markers** - Active emergencies (pulsing)
- **Blue Lines** - Routes from you to emergencies
- **Distance Labels** - Floating distance badges

## 🆓 Free Tier Limits

Mapbox free tier includes:
- ✅ 50,000 map loads per month
- ✅ All map styles
- ✅ No credit card required
- ✅ Perfect for demos and small projects

## 🔧 Troubleshooting

### Map Not Loading?
1. Check your token is correct
2. Make sure it starts with `pk.`
3. Restart the Django server
4. Check browser console for errors (F12)

### "Unauthorized" Error?
- Your token might be invalid
- Get a new token from Mapbox dashboard

### Map Looks Basic?
- Make sure you're using the Mapbox token, not the placeholder
- Clear browser cache (Ctrl + Shift + R)

---

**Once you add your token, the map will look AMAZING!** 🎉
