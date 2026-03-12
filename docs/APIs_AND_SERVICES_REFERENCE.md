# 🔌 Golden Minutes - Complete API & External Services Reference

## 📡 Browser APIs (HTML5/JavaScript)

### 1. **Geolocation API**
**Purpose**: Track user and responder positions in real-time

**Implementation**:
```javascript
// Get current position (one-time)
navigator.geolocation.getCurrentPosition(
    (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const accuracy = position.coords.accuracy;  // meters
        
        // Use coordinates...
    },
    (error) => {
        console.error("Location error:", error.message);
    },
    {
        enableHighAccuracy: true,  // Use GPS (more battery)
        timeout: 10000,            // 10 seconds max
        maximumAge: 0              // Don't use cached position
    }
);

// Watch position (continuous tracking)
const watchId = navigator.geolocation.watchPosition(
    (position) => {
        // Update location every time GPS changes
        updateResponderLocation(position.coords);
    },
    null,
    { enableHighAccuracy: true }
);

// Stop tracking
navigator.geolocation.clearWatch(watchId);
```

**Accuracy**:
- GPS enabled: 5-10 meters
- WiFi/Cell towers: 10-50 meters
- IP-based: 100-5000 meters

**Error Handling**:
- `PERMISSION_DENIED` (1): User rejected permission
- `POSITION_UNAVAILABLE` (2): Location services off
- `TIMEOUT` (3): Took too long to get position

**Files Using This**:
- `static/js/main.js` (SOS trigger)
- `templates/emergencies/map.html` (map tracking)
- `templates/emergencies/detail.html` (ETA calculation)

---

### 2. **Web Speech API**
**Purpose**: Text-to-speech for first-aid voice guidance

**Implementation**:
```javascript
// Check browser support
if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance();
    
    // Set properties
    utterance.text = "Check if the person is breathing";
    utterance.lang = 'en-US';  // or 'hi-IN', 'mr-IN'
    utterance.rate = 1.0;      // Speed (0.1 to 10)
    utterance.pitch = 1.0;     // Pitch (0 to 2)
    utterance.volume = 1.0;    // Volume (0 to 1)
    
    // Event listeners
    utterance.onstart = () => {
        console.log("Speech started");
        // Change button to "⏸ Pause"
    };
    
    utterance.onend = () => {
        console.log("Speech ended");
        // Change button back to "▶ Listen"
    };
    
    utterance.onerror = (event) => {
        console.error("Speech error:", event.error);
    };
    
    // Speak!
    speechSynthesis.speak(utterance);
    
    // Pause/Resume
    speechSynthesis.pause();
    speechSynthesis.resume();
    
    // Stop
    speechSynthesis.cancel();
}
```

**Supported Languages**:
- English (en-US, en-GB)
- Hindi (hi-IN)
- Marathi (mr-IN)
- 50+ other languages

**Browser Support**:
- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support
- ✅ Safari: Full support
- ❌ IE: Not supported

**Files Using This**:
- `templates/emergencies/bystander_guidance.html`

---

### 3. **Device Motion API (Accelerometer)**
**Purpose**: Fall detection using phone's accelerometer

**Implementation**:
```javascript
// Check if device supports motion
if (window.DeviceMotionEvent) {
    window.addEventListener('devicemotion', (event) => {
        const x = event.accelerationIncludingGravity.x;
        const y = event.accelerationIncludingGravity.y;
        const z = event.accelerationIncludingGravity.z;
        
        // Calculate total acceleration
        const totalAcceleration = Math.sqrt(x*x + y*y + z*z);
        
        // Fall detection threshold (2.5g = 24.5 m/s²)
        if (totalAcceleration > 24.5) {
            triggerFallAlert();
        }
    });
}

// iOS 13+ requires permission
if (typeof DeviceMotionEvent.requestPermission === 'function') {
    DeviceMotionEvent.requestPermission()
        .then(permissionState => {
            if (permissionState === 'granted') {
                // Start listening...
            }
        });
}
```

**Physics**:
- 1g = 9.8 m/s² (Earth's gravity)
- Normal activity: 1g - 1.5g
- Running: 1.5g - 2g
- **Fall**: 2.5g+ (sudden impact)

**False Positive Mitigation**:
- Require sustained high acceleration (> 500ms)
- 15-second countdown with alarm sound
- User can cancel false alarm

**Browser Support**:
- ✅ Chrome/Safari on mobile
- ❌ Desktop browsers (no accelerometer)

**Files Using This**:
- `static/js/fall_detection.js`

---

### 4. **Web Audio API**
**Purpose**: Scream/voice detection via microphone analysis

**Implementation**:
```javascript
// Request microphone permission
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        const audioContext = new AudioContext();
        const analyser = audioContext.createAnalyser();
        const microphone = audioContext.createMediaStreamSource(stream);
        
        microphone.connect(analyser);
        analyser.fftSize = 2048;  // Frequency resolution
        
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        
        function analyzeVolume() {
            analyser.getByteFrequencyData(dataArray);
            
            // Calculate average volume
            const volume = dataArray.reduce((a, b) => a + b) / dataArray.length;
            
            // Scream detection (high volume)
            if (volume > 150) {  // Threshold (0-255)
                screamDetected++;
                
                // Sustained scream (2+ seconds)
                if (screamDetected > 20) {  // 20 frames @ 10 FPS
                    triggerVoiceAlert();
                }
            } else {
                screamDetected = 0;  // Reset
            }
            
            requestAnimationFrame(analyzeVolume);
        }
        
        analyzeVolume();
    })
    .catch(error => {
        console.error("Microphone access denied:", error);
    });
```

**Volume Levels**:
- Normal speech: 50-80
- Loud talking: 80-120
- **Scream**: 150-200+

**Privacy**:
- Audio never recorded or transmitted
- Analyzed locally in browser only
- User can disable at any time

**Browser Support**:
- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support
- ⚠️ Safari: Requires HTTPS

**Files Using This**:
- `static/js/voice_trigger.js`

---

### 5. **Push Notifications API**
**Purpose**: Browser notifications even when app is closed

**Implementation**:
```javascript
// Check support
if ('Notification' in window && 'serviceWorker' in navigator) {
    // Request permission
    Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
            // Register service worker
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    // Subscribe to push
                    registration.pushManager.subscribe({
                        userVisibleOnly: true,
                        applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
                    })
                    .then(subscription => {
                        // Send subscription to backend
                        fetch('/api/push-subscribe/', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                subscription: subscription.toJSON(),
                                user_agent: navigator.userAgent
                            })
                        });
                    });
                });
        }
    });
}

// In Service Worker (sw.js)
self.addEventListener('push', event => {
    const data = event.data.json();
    
    const options = {
        body: `${data.emergency_type} - ${data.distance} away`,
        icon: '/static/images/icon-192.png',
        badge: '/static/images/badge-72.png',
        vibrate: [200, 100, 200],  // Vibration pattern
        tag: data.emergency_id,
        requireInteraction: true,  // Stays until dismissed
        actions: [
            { action: 'accept', title: 'Accept', icon: '/static/images/accept.png' },
            { action: 'ignore', title: 'Ignore', icon: '/static/images/ignore.png' }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Emergency Alert!', options)
    );
});

// Notification click
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'accept') {
        clients.openWindow(`/emergencies/${event.notification.tag}/`);
    }
});
```

**VAPID (Voluntary Application Server Identification)**:
- Public key: Sent to browser
- Private key: Kept secret on server
- Validates notifications come from authorized source

**Backend (Python)**:
```python
from pywebpush import webpush, WebPushException
import json

def send_push_notification(subscription, emergency_data):
    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps(emergency_data),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:admin@goldenminutes.com"}
        )
    except WebPushException as e:
        if e.response.status_code == 410:
            # Subscription expired, deactivate
            subscription.is_active = False
            subscription.save()
```

**Browser Support**:
- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support
- ⚠️ Safari: iOS 16.4+ only

**Files Using This**:
- `static/js/notifications.js`
- `static/sw.js` (Service Worker)
- `emergencies/views.py` (backend)

---

### 6. **Service Worker API (PWA)**
**Purpose**: Offline functionality, background sync

**Implementation**:
```javascript
// Register service worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(registration => {
            console.log('Service Worker registered:', registration.scope);
        })
        .catch(error => {
            console.error('Service Worker registration failed:', error);
        });
}

// In service worker (sw.js)
const CACHE_NAME = 'golden-minutes-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/images/logo.png',
    '/offline.html'
];

// Install event (cache files)
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// Fetch event (serve from cache or network)
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return from cache
                if (response) {
                    return response;
                }
                // Not in cache - fetch from network
                return fetch(event.request);
            })
            .catch(() => {
                // Offline and not in cache - show offline page
                return caches.match('/offline.html');
            })
    );
});

// Activate event (clean up old caches)
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
```

**Background Sync** (store SOS when offline):
```javascript
// Register sync
navigator.serviceWorker.ready.then(registration => {
    return registration.sync.register('sync-pending-sos');
});

// In Service Worker
self.addEventListener('sync', event => {
    if (event.tag === 'sync-pending-sos') {
        event.waitUntil(syncPendingSOSes());
    }
});

async function syncPendingSOSes() {
    const db = await openIndexedDB();
    const pendingSOSes = await db.getAll('pendingSOSes');
    
    for (const sos of pendingSOSes) {
        try {
            await fetch('/emergencies/create/', {
                method: 'POST',
                body: JSON.stringify(sos),
                headers: { 'Content-Type': 'application/json' }
            });
            
            // Remove from IndexedDB after successful sync
            await db.delete('pendingSOSes', sos.id);
        } catch (error) {
            console.error('Sync failed:', error);
        }
    }
}
```

**Files Using This**:
- `static/sw.js`
- `static/manifest.json`

---

### 7. **IndexedDB API**
**Purpose**: Store offline SOS data

**Implementation**:
```javascript
// Open database
const request = indexedDB.open('GoldenMinutesDB', 1);

request.onupgradeneeded = (event) => {
    const db = event.target.result;
    
    // Create object store
    if (!db.objectStoreNames.contains('pendingSOSes')) {
        const objectStore = db.createObjectStore('pendingSOSes', { 
            keyPath: 'id', 
            autoIncrement: true 
        });
        
        objectStore.createIndex('timestamp', 'timestamp', { unique: false });
    }
};

request.onsuccess = (event) => {
    const db = event.target.result;
    
    // Store SOS while offline
    function storeSOS(sosData) {
        const transaction = db.transaction(['pendingSOSes'], 'readwrite');
        const objectStore = transaction.objectStore('pendingSOSes');
        
        objectStore.add({
            ...sosData,
            timestamp: Date.now()
        });
        
        transaction.oncomplete = () => {
            console.log('SOS stored offline');
        };
    }
    
    // Retrieve all pending SOSes
    function getPendingSOSes() {
        const transaction = db.transaction(['pendingSOSes'], 'readonly');
        const objectStore = transaction.objectStore('pendingSOSes');
        const request = objectStore.getAll();
        
        request.onsuccess = () => {
            const pendingSOSes = request.result;
            console.log('Pending SOSes:', pendingSOSes);
        };
    }
};
```

---

## 🗺️ Mapping & Geospatial APIs

### 8. **Leaflet.js**
**Purpose**: Interactive map visualization

**Implementation**:
```javascript
// Initialize map
const map = L.map('map').setView([12.9716, 77.5946], 13);  // Bangalore

// Add tile layer (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
}).addTo(map);

// Custom icon
const emergencyIcon = L.icon({
    iconUrl: '/static/images/emergency-marker.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
});

// Add emergency marker
const marker = L.marker([12.9716, 77.5946], { icon: emergencyIcon })
    .addTo(map)
    .bindPopup(`
        <strong>Medical Emergency</strong><br>
        Severity: CRITICAL<br>
        Distance: 1.2 km
    `);

// Add circle overlay (5 km radius)
L.circle([12.9716, 77.5946], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.2,
    radius: 5000  // meters
}).addTo(map);

// Get user location and add marker
map.locate({ setView: true, maxZoom: 16 });

map.on('locationfound', (e) => {
    const userMarker = L.marker(e.latlng, {
        icon: L.icon({
            iconUrl: '/static/images/user-marker.png',
            iconSize: [24, 24]
        })
    }).addTo(map)
      .bindPopup('You are here');
});
```

**Tile Providers** (Map Styles):
- **OpenStreetMap** (Free, no API key)
- **Mapbox** (Requires token, better styling)
- **Google Maps** (Requires API key, most detailed)

**Features Used**:
- Markers with custom icons
- Popups with emergency info
- Circle overlays for radius
- User location tracking
- Clustering (for many markers)

**Files Using This**:
- `templates/emergencies/map.html`
- `static/js/main.js`

---

### 9. **Google Maps Directions API**
**Purpose**: Navigate from responder to emergency

**Implementation**:
```javascript
// Deep link to Google Maps mobile app
const emergencyLat = 12.9716;
const emergencyLon = 77.5946;

const googleMapsURL = `https://www.google.com/maps/dir/?api=1&destination=${emergencyLat},${emergencyLon}&travelmode=driving`;

// Open in new window (or mobile app if installed)
window.open(googleMapsURL, '_blank');
```

**URL Parameters**:
- `destination`: Lat,Lon or address
- `travelmode`: driving, walking, bicycling, transit
- `origin`: Starting point (optional)
- `waypoints`: Intermediate stops (optional)

**No API Key Required** for basic navigation links!

**Files Using This**:
- `templates/emergencies/detail.html` (Navigate button)

---

## 🔐 Authentication & Security APIs

### 10. **Django Authentication System**
**Purpose**: User login, registration, session management

**Key Features**:
- **Password Hashing**: PBKDF2 algorithm (100,000 iterations)
- **Session Management**: Secure cookies with CSRF protection
- **Permission System**: User groups and permissions

**Implementation**:
```python
# Login
from django.contrib.auth import authenticate, login

user = authenticate(username=username, password=password)
if user is not None:
    login(request, user)
    # User is now logged in
```

**Security Features**:
- CSRF tokens on all forms
- SQL injection prevention (ORM)
- XSS protection (template auto-escaping)
- Clickjacking protection (X-Frame-Options)

---

## 📊 Third-Party Libraries

### 11. **Bootstrap 5**
**Purpose**: Responsive CSS framework

**CDN**:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

**Components Used**:
- Grid system (12-column)
- Cards, Badges, Alerts
- Modal dialogs
- Navigation bars
- Form controls

---

### 12. **Chart.js** (Future - Analytics Dashboard)
**Purpose**: Data visualization for analytics

**Implementation**:
```javascript
const ctx = document.getElementById('responseChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
            label: 'Emergencies Responded',
            data: [5, 8, 12, 15, 18],
            borderColor: 'rgb(220, 53, 69)',
            backgroundColor: 'rgba(220, 53, 69, 0.2)'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: true },
            title: { display: true, text: 'Response History' }
        }
    }
});
```

---

## 🌐 External Services (Future Integration)

### 13. **Twilio API** (SMS Notifications)
**Purpose**: Send SMS alerts when push fails

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Emergency alert: Medical emergency 1.2 km from you. Open app to respond.",
    from_='+1234567890',
    to=responder.phone_number
)
```

---

### 14. **SendGrid API** (Email Notifications)
**Purpose**: Email summaries, weekly reports

```python
import sendgrid
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='noreply@goldenminutes.com',
    to_emails=user.email,
    subject='Weekly Emergency Summary',
    html_content='<strong>You responded to 5 emergencies this week!</strong>'
)

sg = sendgrid.SendGridAPIClient(api_key)
response = sg.send(message)
```

---

### 15. **Firebase Cloud Messaging (FCM)** (Native App)
**Purpose**: Push notifications for native Android/iOS apps

```python
import firebase_admin
from firebase_admin import messaging

message = messaging.Message(
    notification=messaging.Notification(
        title='Emergency Alert!',
        body='Medical emergency 1.2 km away',
    ),
    token=device_token,
)

response = messaging.send(message)
```

---

## 📋 API Usage Summary

| API | Category | Purpose | Cost |
|-----|----------|---------|------|
| Geolocation | Browser | GPS tracking | Free |
| Web Speech | Browser | Voice guidance | Free |
| Device Motion | Browser | Fall detection | Free |
| Web Audio | Browser | Scream detection | Free |
| Push Notifications | Browser | Alerts | Free |
| Service Worker | Browser | Offline PWA | Free |
| IndexedDB | Browser | Offline storage | Free |
| Leaflet.js | Mapping | Map display | Free |
| OpenStreetMap | Mapping | Map tiles | Free |
| Google Maps Navigate | Mapping | Directions | Free (link-only) |
| Django Auth | Backend | User management | Free |
| Bootstrap 5 | Frontend | Responsive UI | Free |
| pywebpush | Backend | Push server | Free |
| Twilio | External | SMS (future) | Paid |
| SendGrid | External | Email (future) | Paid |
| FCM | External | Native push (future) | Free |

---

## 🚀 No API Keys Required for MVP!

**Current Implementation Uses Only Free APIs:**
- ✅ Browser APIs (built-in)
- ✅ Leaflet.js + OpenStreetMap (open-source)
- ✅ Google Maps navigation (basic links)
- ✅ Django (self-hosted)
- ✅ Bootstrap (CDN)

**Optional (Enhanced Features):**
- Mapbox (better map styling): $5/month for 100K requests
- Google Maps API (traffic data): $200 free credit/month
- Twilio (SMS): $0.0075/SMS
- SendGrid (email): 100 emails/day free

---

**This covers ALL APIs and external services used in the Golden Minutes project!** 🎯
