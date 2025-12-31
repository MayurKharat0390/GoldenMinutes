# Golden Minutes Deployment Guide

## 1. Environment Setup
Golden Minutes is a Django 5.x application.

### Requirements:
- Python 3.12+
- PostgreSQL (Recommended for production)
- Redis (Optional, for caching if needed later)

### Environment Variables (.env)
Create a `.env` file in the root directory:
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=goldenminutes.com,www.goldenminutes.com
DATABASE_URL=postgres://user:pass@localhost:5432/golden_minutes
GM_MAPS_API_KEY=your-google-maps-key
```

## 2. Static Files
For production (e.g., Nginx/Apache), collect static files:
```bash
python manage.py collectstatic
```

## 3. Serving the App
Use `gunicorn` or `uvicorn`:
```bash
pip install gunicorn
gunicorn golden_minutes.wsgi:application --bind 0.0.0.0:8000
```

## 4. HTTPS (Critical)
Since we use Geolocation APIs and Notification APIs, **HTTPS is required**.
- Use **Nginx** as a reverse proxy with Let's Encrypt / Certbot.
- Browser functionality (Popups, Location) will BLOCK on unsecured HTTP/IPs (except localhost).

## 5. Security Checklist
- [ ] Change the Admin URL path.
- [ ] Set `SECURE_SSL_REDIRECT = True` in settings.
- [ ] Disable the `populate_*.py` scripts in production.

## 6. Features Note
- **Notifications**: Rely on frontend polling (`check_new_emergencies`). Ensure the user keeps the tab open.
- **Maps**: Ensure your Google Maps API key has billing enabled.

---
*Built with ❤️ by AntiGravity Agent*
