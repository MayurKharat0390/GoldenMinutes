# 📂 Golden Minutes - Complete File Structure & Purpose

## 🗂️ Project Organization

```
Golden Minutes/
├── 📁 accounts/              # User authentication & profiles app
├── 📁 emergencies/           # Emergency management app
├── 📁 responders/            # Volunteer management app
├── 📁 training/              # Training modules app
├── 📁 golden_minutes/        # Main project configuration
├── 📁 templates/             # HTML templates
├── 📁 static/                # CSS, JavaScript, images
├── 📁 media/                 # User uploads (profile pics, etc.)
├── 📁 locale/                # Translations (Hindi, Marathi)
├── 📁 docs/                  # Documentation
├── 📄 manage.py              # Django management script
├── 📄 requirements.txt       # Python dependencies
├── 📄 db.sqlite3             # Database file
└── 📄 Procfile               # Deployment configuration
```

---

## 📁 accounts/ - User Management App

### **Models** (accounts/models.py)
```python
User - Custom user model extending AbstractUser
  - email, phone_number, role (CITIZEN/VOLUNTEER/ADMIN)
  - latitude, longitude (location)
  - profile_picture, bio
  - consent_given, created_at, updated_at
```

### **Views** (accounts/views.py)
- `register()` - User registration
- `user_login()` - User login
- `user_logout()` - User logout
- `profile()` - View/edit profile
- `delete_account()` - Account deletion

### **Templates** (accounts/)
- `register.html` - Registration form
- `login.html` - Login form
- `profile.html` - User profile page

### **URLs** (accounts/urls.py)
```
/accounts/register/
/accounts/login/
/accounts/logout/
/accounts/profile/
/accounts/delete/
```

---

## 📁 emergencies/ - Emergency Management App

### **Models** (emergencies/models.py)
```python
Emergency - Core emergency model
  - emergency_id (UUID), victim (ForeignKey)
  - emergency_type (MEDICAL/ACCIDENT/FIRE/PERSONAL/DISASTER)
  - severity (LOW/MEDIUM/HIGH/CRITICAL)
  - status (ACTIVE/RESPONDED/RESOLVED/CANCELLED)
  - latitude, longitude, address, city, state
  - description, bystander_mode_active
  - created_at, updated_at

EmergencyResponse - Responder actions
  - response_id (UUID), emergency (ForeignKey), responder (ForeignKey)
  - status (ACCEPTED/EN_ROUTE/ARRIVED/COMPLETED)
  - distance_km, estimated_arrival_minutes
  - actual_arrival_time, notes

EmergencyTimeline - Audit log
  - emergency (ForeignKey), event_type, description
  - actor (ForeignKey to User), created_at

BystanderGuidance - First-aid instructions
  - emergency_type, title, step_number
  - instruction, icon_class, warning

PushSubscription - Push notification subscriptions
  - user (ForeignKey), subscription_info (JSONField)
  - notification_radius_km, is_active

ResponderLocation - Live GPS tracking
  - responder (OneToOneField), latitude, longitude
  - accuracy, updated_at
```

### **Views** (emergencies/views.py)
- `emergency_list()` - List all emergencies
- `emergency_detail()` - Emergency detail page
- `emergency_create()` - Create new emergency (SOS trigger)
- `emergency_map()` - Live map view
- `accept_emergency()` - Volunteer accepts emergency
- `mark_arrived()` - Volunteer marks arrival
- `resolve_emergency()` - Mark emergency as resolved
- `bystander_guidance()` - First-aid instructions
- `api_push_subscribe()` - Save push subscription
- `api_responder_location()` - Get responder GPS
- `api_update_responder_location()` - Update responder GPS

### **Templates** (emergencies/)
- `list.html` - Emergency list
- `detail.html` - Emergency detail with map
- `map.html` - Full-screen live map
- `create.html` - SOS trigger page
- `bystander_guidance.html` - First-aid steps

### **URLs** (emergencies/urls.py)
```
/emergencies/
/emergencies/<uuid>/
/emergencies/create/
/emergencies/map/
/emergencies/<uuid>/accept/
/emergencies/<uuid>/arrived/
/emergencies/<uuid>/resolve/
/emergencies/<uuid>/bystander/
/emergencies/api/push-subscribe/
/emergencies/api/responder-location/<id>/
/emergencies/api/update-location/
```

### **Management Commands** (emergencies/management/commands/)
- `activate_bystander_mode.py` - Auto-activate bystander mode after timeout

---

## 📁 responders/ - Volunteer Management App

### **Models** (responders/models.py)
```python
VolunteerProfile - Volunteer information
  - user (OneToOneField), verification_status (PENDING/VERIFIED/REJECTED)
  - certification_type (FIRST_AID/PARAMEDIC/DOCTOR/FIREFIGHTER)
  - certification_number, verification_document
  - availability_radius_km, is_available
  - level, total_points, total_responses, successful_responses
  - current_streak_days, longest_streak_days, last_active_date

ResponderStats - Detailed analytics
  - responder (OneToOneField), total_responses, successful_responses
  - cancelled_responses, average_response_time_minutes
  - total_distance_traveled_km, lives_impacted
  - badges (ManyToManyField)

Badge - Achievement badges
  - name, category (MILESTONE/PERFORMANCE/SPECIAL/TRAINING)
  - description, requirement_type, requirement_value
  - icon_class, points_awarded

AreaSafetyScore - Community safety metrics
  - area (CharField), city, state
  - safety_score (1-10), total_emergencies
  - avg_response_time_minutes, active_volunteers
```

### **Views** (responders/views.py)
- `volunteer_dashboard()` - Volunteer dashboard
- `volunteer_apply()` - Apply to become volunteer
- `volunteer_leaderboard()` - Top volunteers
- `volunteer_stats()` - Individual stats
- `badge_list()` - Available badges
- `admin_verify_volunteer()` - Admin approve/reject

### **Templates** (responders/)
- `dashboard.html` - Volunteer dashboard
- `apply.html` - Volunteer application form
- `leaderboard.html` - Leaderboard
- `stats.html` - Volunteer statistics
- `badges.html` - Badge showcase

### **URLs** (responders/urls.py)
```
/responders/dashboard/
/responders/apply/
/responders/leaderboard/
/responders/stats/
/responders/badges/
/admin/verify/<id>/
```

---

## 📁 training/ - Training Modules App

### **Models** (training/models.py)
```python
TrainingModule - Educational content
  - title, slug, description, content (HTML)
  - video_url (YouTube embed), duration_minutes
  - category (FIRST_AID/CPR/EMERGENCY_RESPONSE/SAFETY)
  - difficulty_level (BEGINNER/INTERMEDIATE/ADVANCED)
  - order (display order), is_published

UserProgress - Track user learning
  - user (ForeignKey), module (ForeignKey)
  - status (NOT_STARTED/IN_PROGRESS/COMPLETED)
  - progress_percentage, started_at, completed_at
```

### **Views** (training/views.py)
- `module_list()` - List all training modules
- `module_detail()` - View module content
- `start_module()` - Start training
- `complete_module()` - Mark as complete
- `my_progress()` - User's training progress

### **Templates** (training/)
- `module_list.html` - Training catalog
- `module_detail.html` - Module content viewer
- `my_progress.html` - Progress dashboard

### **URLs** (training/urls.py)
```
/training/
/training/<slug>/
/training/<slug>/start/
/training/<slug>/complete/
/training/my-progress/
```

---

## 📁 golden_minutes/ - Main Project Config

### **settings.py** - Django configuration
```python
# Key settings:
- INSTALLED_APPS (all Django apps)
- DATABASES (SQLite/PostgreSQL)
- MIDDLEWARE (security, sessions, i18n)
- TEMPLATES (template directories)
- STATIC_URL, STATICFILES_DIRS
- LANGUAGE_CODE, LANGUAGES (i18n)
- EMERGENCY_RADIUS_KM (5 km)
- EMERGENCY_TIMEOUT_MINUTES (5 min)
- VAPID keys for push notifications
```

### **urls.py** - Main URL routing
```python
# Routes:
/admin/                    → Django admin
/accounts/                 → User auth
/emergencies/              → Emergency system
/responders/               → Volunteer features
/training/                 → Training modules
/i18n/setlang/             → Language switcher
/                          → Homepage
```

### **wsgi.py** - WSGI application
- Entry point for production deployment (Gunicorn/uWSGI)

---

## 📁 templates/ - HTML Templates

### **Base Templates**
- `base.html` - Main layout (navbar, footer, scripts)
- `home.html` - Homepage with hero section

### **PWA Templates**
- `offline.html` - Offline fallback page
- `manifest.json` - PWA manifest (in static/)

---

## 📁 static/ - Static Assets

### **CSS** (static/css/)
- `style.css` - Custom styles
  - Glassmorphism effects
  - Animations (@keyframes)
  - Responsive media queries

### **JavaScript** (static/js/)
- `main.js` - Core functionality
  - SOS trigger
  - Map initialization (Leaflet.js)
  - Real-time updates
  - Distance calculations (Haversine)

- `notifications.js` - Push notifications
  - Permission request
  - Subscription management
  - VAPID integration

- `fall_detection.js` - Accelerometer monitoring
  - Device motion listening
  - Fall threshold detection (2.5g)
  - Alert countdown timer

- `voice_trigger.js` - Voice/scream detection
  - Microphone access
  - Audio analysis (Web Audio API)
  - Volume threshold monitoring

### **Images** (static/images/)
- `logo.png` - App logo
- `icon-192.png`, `icon-512.png` - PWA icons
- `hero-background.jpg` - Homepage hero image
- Custom markers for map

### **Service Worker** (static/)
- `sw.js` - Service Worker script
  - Offline caching
  - Push notification handling
  - Background sync

### **PWA Manifest** (static/)
- `manifest.json` - PWA configuration
  - App name, short_name
  - Icons, theme color
  - Display mode: standalone

---

## 📁 locale/ - Translations

### **Hindi** (locale/hi/LC_MESSAGES/)
- `django.po` - Translation strings (source)
- `django.mo` - Compiled translations (binary)

### **Marathi** (locale/mr/LC_MESSAGES/)
- `django.po` - Translation strings (source)
- `django.mo` - Compiled translations (binary)

---

## 📁 docs/ - Project Documentation

### **Complete Guides** (30+ files)
1. `README.md` - Main readme
2. `PROJECT_SUMMARY.md` - Project overview
3. `FEATURES_IMPLEMENTED.md` - Feature list
4. `ADVANCED_FEATURES.md` - Advanced features guide
5. `MULTI_LANGUAGE_COMPLETE.md` - i18n setup
6. `DASHBOARD_COMPLETE.md` - Dashboard guide
7. `AUTO_BADGES_COMPLETE.md` - Gamification system
8. `BYSTANDER_MULTILANGUAGE.md` - Bystander mode
9. `TESTING_GUIDE.md` - Testing instructions
10. `RAILWAY_DEPLOYMENT.md` - Deployment guide
11. `ANDROID_APP_GUIDE.md` - Native app guide
12. `MAPBOX_SETUP.md` - Map configuration

### **CEP Exhibition Docs** (Created Today!)
1. `CEP_EXHIBITION_GUIDE.md` - Complete project documentation
2. `QUICK_REFERENCE_PANEL_QA.md` - Panel questions & answers
3. `SYSTEM_ARCHITECTURE_DIAGRAMS.md` - Architecture flowcharts
4. `APIs_AND_SERVICES_REFERENCE.md` - API documentation

---

## 📄 Root Files

### **manage.py**
Django's command-line utility:
```bash
python manage.py runserver        # Start dev server
python manage.py migrate          # Apply migrations
python manage.py createsuperuser  # Create admin
python manage.py makemigrations   # Generate migrations
python manage.py collectstatic    # Collect static files
python manage.py compilemessages  # Compile translations
```

### **requirements.txt**
Python dependencies (70+ packages):
```
Django==5.1.4
djangorestframework==3.15.2
django-cors-headers==4.6.0
dj-database-url==2.3.0
psycopg2-binary==2.9.10
gunicorn==23.0.0
whitenoise==6.8.2
pywebpush==2.0.1
python-dateutil==2.9.0
Pillow==11.0.0
```

### **Procfile**
Railway/Heroku deployment:
```
web: gunicorn golden_minutes.wsgi --log-file -
release: python manage.py migrate
```

### **runtime.txt**
Python version:
```
python-3.10.11
```

### **.gitignore**
Excluded files:
```
db.sqlite3
__pycache__/
*.pyc
media/
staticfiles/
.env
venv/
```

---

## 🗄️ Database File

### **db.sqlite3**
SQLite database (311 KB):
- 15+ tables (including Django defaults)
- Demo data:
  - 5 demo citizens
  - 5 demo volunteers
  - 32 first-aid steps
  - 13 badges
  - Sample emergencies

---

## 📊 Utility Scripts (Root Directory)

### **Data Population Scripts**
1. `populate_first_aid.py` - Add 32 first-aid steps
2. `populate_badges.py` - Create 13 achievement badges
3. `populate_training.py` - Add training modules

### **Testing Scripts**
1. `create_test_emergencies.py` - Generate test emergencies
2. `create_demo_emergencies.py` - Demo emergencies with responses
3. `test_bystander.py` - Test bystander mode activation
4. `test_auto_badges.py` - Test badge auto-award logic

### **Admin Scripts**
1. `create_admin.py` - Create superuser programmatically
2. `fix_missing_profiles.py` - Fix orphaned user profiles
3. `cleanup_emergencies.py` - Clean old emergencies

### **Translation Scripts**
1. `add_hindi_translations.py` - Add Hindi translations
2. `add_bystander_translations.py` - Translate first-aid steps
3. `check_translations.py` - Verify translation completeness

### **Security Scripts**
1. `generate_vapid_keys.py` - Generate push notification keys

---

## 📈 File Statistics

### **By Type**
- **Python files**: 60+
- **HTML templates**: 22
- **JavaScript files**: 4
- **CSS files**: 1 (+ Bootstrap CDN)
- **Documentation files**: 35+
- **Total lines of code**: ~5,000

### **By App**
- **accounts/**: 300 lines
- **emergencies/**: 1,500 lines
- **responders/**: 1,200 lines
- **training/**: 400 lines
- **templates/**: 1,000 lines
- **static/js**: 600 lines

---

## 🔑 Key Files for Demo

### **Must Know Well**
1. `emergencies/models.py` - Emergency model + severity AI
2. `emergencies/views.py` - SOS trigger, responder matching
3. `static/js/main.js` - Frontend SOS logic, map
4. `responders/models.py` - Gamification system
5. `templates/base.html` - UI structure

### **Nice to Know**
1. `settings.py` - Configuration
2. `requirements.txt` - Dependencies
3. `docs/CEP_EXHIBITION_GUIDE.md` - This guide!

---

## 🎯 Total Project Size

```
Golden Minutes/
├── Source Code:       ~5,000 lines
├── Documentation:     ~10,000 lines
├── Database:          311 KB
├── Static Assets:     ~2 MB
├── Dependencies:      ~150 MB (venv)
└── TOTAL:             ~152 MB
```

---

**You now have a complete understanding of every file in the project!** 🚀
