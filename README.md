# 🚨 Golden Minutes - Emergency Response Network

**Decentralized, Community-Driven Emergency Response System**

Golden Minutes is a Django-based web application that connects emergency victims with nearby trained volunteers in critical moments, reducing response times and saving lives.

---

## 🎯 **Core Features**

### ✅ **Implemented:**
1. **Real-Time Emergency Alerts** - Instant SOS with GPS location
2. **Live Map View** - See emergencies and responders in real-time
3. **Smart Responder Matching** - Nearest available volunteers notified
4. **Enhanced Volunteer Dashboard** - Gamification, badges, leaderboard
5. **First-Aid Guidance** - Step-by-step instructions for bystanders
6. **Smart Bystander Mode** - Auto-activates if no responder arrives
7. **Multi-Language Support** - English, Hindi (हिंदी), Marathi (मराठी)
8. **Push Notifications** - Real-time alerts for volunteers
9. **PWA Support** - Install as mobile app
10. **Offline Mode** - Works without internet

---

## 🚀 **Quick Start**

### Prerequisites:
- Python 3.10+
- Django 5.1.4
- SQLite (default) or PostgreSQL

### Installation:

```bash
# Clone the repository
git clone <repository-url>
cd "Golden Minutes"

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate test data
python populate_first_aid.py
python populate_badges.py

# Start server
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## 📚 **Documentation**

All documentation is in the [`docs/`](./docs/) folder:

### Getting Started:
- [Quick Start Guide](./docs/QUICK_START.md)
- [Features Implemented](./docs/FEATURES_IMPLEMENTED.md)
- [Testing Guide](./docs/TESTING_GUIDE.md)

### Feature Documentation:
- [Advanced Features](./docs/ADVANCED_FEATURES.md)
- [Enhanced Dashboard](./docs/DASHBOARD_COMPLETE.md)
- [Multi-Language Support](./docs/MULTI_LANGUAGE_COMPLETE.md)
- [Bystander Mode Testing](./docs/TESTING_BYSTANDER_MODE.md)

### Deployment:
- [Railway Deployment](./docs/RAILWAY_DEPLOYMENT.md)
- [Android App Guide](./docs/ANDROID_APP_GUIDE.md)

### Development:
- [Implementation Plan](./docs/COMPLETE_IMPLEMENTATION_PLAN.md)
- [Project Summary](./docs/PROJECT_SUMMARY.md)

---

## 🎮 **Tech Stack**

**Backend:**
- Django 5.1.4
- Django REST Framework
- SQLite / PostgreSQL

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Leaflet.js (Maps)
- Web Speech API (Voice)

**Features:**
- PWA (Progressive Web App)
- Push Notifications
- Geolocation API
- Service Workers

---

## 🌟 **Key Highlights**

### Gamification System:
- **Points & Levels** - Earn points for responses
- **13 Achievement Badges** - Milestone, Performance, Special, Training
- **Leaderboard** - Compete with other volunteers
- **Streak Tracking** - Consecutive days active

### Emergency Types:
- Medical Emergency (CPR, Heart Attack, etc.)
- Accident (Bleeding, Fractures, etc.)
- Fire (Burns, Smoke Inhalation, etc.)
- Personal Safety (Assault, Harassment, etc.)
- Disaster (Earthquake, Flood, etc.)

### First-Aid Instructions:
- 32 comprehensive steps
- Voice guidance (Text-to-Speech)
- Progress tracking
- Visual warnings
- Emergency contact quick-dial

---

## 📱 **Mobile App**

Golden Minutes works as a Progressive Web App (PWA):

1. **Visit** the website on mobile
2. **Click** "Add to Home Screen"
3. **Use** like a native app

For native Android app, see [Android App Guide](./docs/ANDROID_APP_GUIDE.md)

---

## 🌐 **Multi-Language**

Supports 3 languages:
- **English** (Default)
- **हिंदी** (Hindi)
- **मराठी** (Marathi)

Language switcher in navigation bar.

---

## 🧪 **Testing**

```bash
# Run tests
python manage.py test

# Create test emergencies
python create_test_emergencies.py

# Activate bystander mode
python test_bystander.py
```

See [Testing Guide](./docs/TESTING_GUIDE.md) for details.

---

## 📊 **Project Structure**

```
Golden Minutes/
├── accounts/           # User authentication & profiles
├── emergencies/        # Emergency management
├── responders/         # Volunteer management
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── locale/            # Translations (hi, mr)
├── docs/              # Documentation
└── manage.py          # Django management
```

---

## 🤝 **Contributing**

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 **License**

This project is open source and available under the MIT License.

---

## 🆘 **Support**

For issues or questions:
- Check [Documentation](./docs/)
- Open an issue on GitHub
- Contact the development team

---

## 🎯 **Roadmap**

### Phase 1 (Completed):
- ✅ Core emergency system
- ✅ Volunteer dashboard
- ✅ First-aid guidance
- ✅ Multi-language support

### Phase 2 (Planned):
- ⏳ Analytics dashboard
- ⏳ Training modules
- ⏳ Hospital integration
- ⏳ Video instructions

### Phase 3 (Future):
- 🔮 AI chatbot
- 🔮 Predictive analytics
- 🔮 Community forums
- 🔮 Certification system

---

## 🏆 **Achievements**

- **4 Major Features** implemented
- **32 First-Aid Steps** documented
- **13 Achievement Badges** created
- **3 Languages** supported
- **PWA Ready** for mobile

---

**Built with ❤️ for saving lives in critical moments**

**Every second counts. Every volunteer matters.** 🚨

---

*Last Updated: December 31, 2025*
