# Golden Minutes - Emergency Response System

## 🚨 Project Overview

**Golden Minutes** is a location-aware emergency response system that connects emergency victims with verified nearby responders during the critical "golden hour" before official emergency services arrive.

This is a **Computer Engineering Project (CEP)** demonstrating:
- Real-world problem solving
- Clean system architecture
- Practical feature implementation
- Ethical & legal awareness
- Working web demonstration

## ⚠️ Important Disclaimer

**This system assists during emergencies and does NOT replace official emergency services.**  
Always call **112** (India Emergency Number) for police, ambulance, or fire services.

## 🎯 Problem Statement

Emergency services often face delays due to:
- **Traffic congestion** - Ambulances stuck in traffic
- **Distance** - Nearest hospital too far away
- **Overload** - Peak hours and disaster situations

People lose their lives in the **"golden minutes"** before help arrives. This system fills the response gap by activating verified nearby responders and trained volunteers until authorities arrive.

## 🛠️ Tech Stack

### Backend
- **Django 5.1.4** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (acceptable for CEP)
- **Python 3.x**

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **Bootstrap 5.3.2** - Responsive framework
- **Vanilla JavaScript** - Interactivity
- **Leaflet.js** - Interactive maps

### PWA
- **Manifest.json** - App metadata
- **Service Worker** - Offline support
- **IndexedDB** - Offline SOS storage

## 👥 User Roles

1. **Citizen/Victim** - Can trigger SOS emergencies
2. **Volunteer/Responder** - Verified helpers who respond to emergencies
3. **Admin** - System management and volunteer verification

## ✨ Features Implemented

### 1️⃣ SOS Emergency Trigger
- One-tap SOS button (fixed position, always accessible)
- Automatic GPS location capture
- Emergency type selection (Accident, Medical, Fire, Personal Safety, Disaster)
- Optional text/voice input
- Stores as Emergency event

### 2️⃣ Emergency Type Selection
- 5 emergency categories
- Each feeds into severity classification

### 3️⃣ AI-Inspired Severity Classification
- **Rule-based engine** (no external AI calls)
- Classifies as: Critical / High / Moderate / Low
- Example rules:
  - Fire → Critical
  - Medical → High
  - Accident → Moderate

### 4️⃣ Live Emergency Map
- Interactive Leaflet.js map
- Shows active emergencies
- Shows responders en route
- Role-based visibility (public limited, responders full access)

### 5️⃣ Responder Matching & Race Mode
- Identifies responders within configurable radius (default: 5km)
- Shows distance and ETA
- First responder to accept becomes Primary Responder
- Others are notified if primary declines

### 6️⃣ Volunteer Registration & Verification
- Signup form with ID upload
- Certification upload (optional)
- Role levels:
  - General Volunteer
  - First-Aid Trained
  - Medical Professional
- Admin approval workflow

### 7️⃣ Volunteer Dashboard
- Incoming emergency alerts
- Accept/Decline emergency
- View route to location
- Emergency response history

### 8️⃣ Smart Bystander Mode
- Activates if no responder accepts within timeout (default: 5 minutes)
- Shows guided instructions:
  - CPR steps
  - Bleeding control
  - Do's & Don'ts
- Text + icons (web-friendly)

### 9️⃣ Life Impact Score
- Each volunteer has impact score based on:
  - Number of responses (40%)
  - Success rate (30%)
  - Timeliness (20%)
  - Role level (10%)
- Displayed on profile
- **No money, no gambling, no competition pressure**

### 🔟 Emergency Timeline & Logs
- Complete audit trail for each emergency:
  - SOS triggered time
  - Responder accepted time
  - Arrival time
  - Status updates
- Used for learning and demo credibility

### 1️⃣1️⃣ Community Safety Score
- Area-based metric calculated from:
  - Volunteer density (50%)
  - Average response time (30%)
  - Resolution rate (20%)
- Color-coded: Green / Yellow / Orange / Red

### 1️⃣2️⃣ PWA Support
- Add to Home Screen
- Offline SOS storage (IndexedDB)
- Auto-send when back online
- Background sync

## 📁 Project Structure

```
golden_minutes/
├── accounts/                 # User authentication & profiles
│   ├── models.py            # Custom User model
│   ├── views.py             # Auth views
│   ├── urls.py              # Auth URLs
│   └── admin.py             # User admin
├── emergencies/             # Emergency management
│   ├── models.py            # Emergency, Response, Timeline, Guidance
│   ├── views.py             # SOS, map, timeline views
│   ├── urls.py              # Emergency URLs
│   └── admin.py             # Emergency admin
├── responders/              # Volunteer/responder management
│   ├── models.py            # VolunteerProfile, AreaSafetyScore
│   ├── views.py             # Dashboard, leaderboard
│   ├── urls.py              # Responder URLs
│   └── admin.py             # Volunteer verification admin
├── golden_minutes/          # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   └── wsgi.py              # WSGI config
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Landing page
│   └── pwa/                 # PWA files
│       ├── manifest.json    # PWA manifest
│       └── sw.js            # Service worker
├── static/                  # Static files
│   ├── css/
│   │   └── main.css         # Main stylesheet
│   ├── js/
│   │   └── main.js          # Main JavaScript
│   └── images/              # Icons and images
├── media/                   # User uploads
├── manage.py                # Django management
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🗄️ Database Schema

### User Model
- Extended Django AbstractUser
- Fields: role, phone_number, latitude, longitude, terms_accepted

### VolunteerProfile Model
- One-to-one with User
- Fields: role_level, verification_status, id_document, certification, impact_score

### Emergency Model
- Fields: emergency_id (UUID), victim, emergency_type, severity, status, location, timestamps

### EmergencyResponse Model
- Tracks responder interactions
- Fields: emergency, responder, status, distance_km, ETA

### EmergencyTimeline Model
- Audit log for all emergency events
- Fields: emergency, event_type, description, actor, timestamp

### BystanderGuidance Model
- Pre-populated first-aid instructions
- Fields: emergency_type, step_number, instruction, warning

### AreaSafetyScore Model
- Community safety metrics
- Fields: area_name, location, volunteer_count, safety_score, score_color

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone/Navigate to project directory**
```bash
cd "d:\Golden Minutes"
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (admin)**
```bash
python manage.py createsuperuser
```

6. **Load demo data (optional)**
```bash
python manage.py loaddata demo_data.json
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📱 PWA Installation

1. Open the site in Chrome/Edge on mobile
2. Tap "Add to Home Screen"
3. App will work offline with limited functionality

## 🎨 Design Philosophy

- **Reliability > Flashiness**
- **Safety > Speed**
- **Clarity > Complexity**
- **Demo-friendly > Fully automated**

## 🔒 Legal & Ethical Considerations

1. **Clear Disclaimer**: System does not replace official emergency services
2. **Explicit Consent**: Users must accept terms before triggering SOS
3. **Role-based Restrictions**: Volunteers cannot perform invasive medical actions
4. **Data Privacy**: Location data only stored with consent
5. **Verification Required**: All responders must be verified by admin

## 🎓 Academic Context

This project demonstrates:
- **Problem Understanding**: Addresses real-world emergency response gaps
- **System Architecture**: Clean separation of concerns (accounts, emergencies, responders)
- **Practical Implementation**: Working features, not just theory
- **Ethical Awareness**: Legal disclaimers, consent, verification
- **Technical Depth**: Django, REST APIs, PWA, geolocation, real-time updates

## 📊 Demo Data

To populate the system with demo data for presentation:

```bash
python manage.py shell
```

Then run the demo data script (to be created).

## 🔧 Configuration

Key settings in `golden_minutes/settings.py`:

```python
EMERGENCY_RADIUS_KM = 5  # Search radius for nearby responders
EMERGENCY_TIMEOUT_MINUTES = 5  # Time before activating bystander mode
MAX_RESPONDERS_TO_NOTIFY = 10  # Maximum responders per emergency
```

## 📝 API Endpoints

- `GET /emergencies/api/active/` - Get active emergencies
- `GET /emergencies/api/<uuid>/status/` - Get emergency status
- `POST /accounts/update-location/` - Update user location
- `POST /responders/api/toggle-availability/` - Toggle responder availability

## 🎯 Success Metrics

- Average response time < 5 minutes
- 90%+ emergency resolution rate
- High volunteer retention
- Positive user feedback

## 🚧 Future Enhancements

- SMS/Push notifications
- Voice-to-text for emergency description
- Multi-language support
- Integration with official emergency services
- Advanced analytics dashboard
- Mobile native apps (Android/iOS)

## 👨‍💻 Development Team

This is an academic project for Computer Engineering evaluation.

## 📄 License

This is an academic project. Not for commercial use.

## 🙏 Acknowledgments

- Bootstrap for responsive UI
- Leaflet.js for mapping
- Django community for excellent documentation
- All emergency responders who inspired this project

---

**Remember: This system assists during emergencies but does NOT replace calling 112 (India Emergency Number).**
