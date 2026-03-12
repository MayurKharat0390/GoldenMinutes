# 🏗️ Golden Minutes - System Architecture & Flow Diagrams

## 📊 High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│   │   Citizens   │  │  Volunteers  │  │    Admins    │            │
│   │  (Victims)   │  │ (Responders) │  │  (System)    │            │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│          │                  │                  │                     │
│    - Trigger SOS       - Accept SOS      - Manage Users            │
│    - View Map          - View Map        - Verify Volunteers       │
│    - Get Guidance      - Track ETA       - Monitor Emergencies     │
│                        - Earn Badges     - View Analytics          │
└─────────┼────────────────────┼────────────────────┼────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                             │
│                   (HTML5 + CSS3 + JavaScript)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │  Templates    │  │  Static Files │  │  Service      │          │
│  │  (Django)     │  │  (Bootstrap)  │  │  Worker       │          │
│  │               │  │               │  │  (PWA)        │          │
│  │ - base.html   │  │ - CSS         │  │ - Offline     │          │
│  │ - map.html    │  │ - JavaScript  │  │ - Push        │          │
│  │ - dashboard   │  │ - Leaflet.js  │  │ - Sync        │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
└─────────┼────────────────────────────────────────┼──────────────────┘
          │                                        │
          ▼                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                              │
│                (Django 5.1.4 + Django REST Framework)               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Accounts │  │Emergency │  │Responders│  │ Training │           │
│  │   App    │  │   App    │  │   App    │  │   App    │           │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤           │
│  │- Auth    │  │- SOS     │  │- Profile │  │- Modules │           │
│  │- Profile │  │- Matching│  │- Badges  │  │- Progress│           │
│  │- Consent │  │- Timeline│  │- Stats   │  │- Certs   │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                      │
│  ┌───────────────────────────────────────────────────────┐         │
│  │           Core Business Logic                         │         │
│  │  - Severity Classification (Rule-Based AI)            │         │
│  │  - Responder Matching Algorithm                       │         │
│  │  - Badge Auto-Award System                            │         │
│  │  - Bystander Mode Activation                          │         │
│  └───────────────────────────────────────────────────────┘         │
│                                                                      │
└─────────┼───────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                   │
│               (SQLite / PostgreSQL + ORM)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                   │
│  │    User    │  │ Emergency  │  │ Volunteer  │                   │
│  │            │  │            │  │  Profile   │                   │
│  │- email     │  │- type      │  │- verified  │                   │
│  │- role      │  │- severity  │  │- level     │                   │
│  │- location  │  │- status    │  │- points    │                   │
│  └────────────┘  └────────────┘  └────────────┘                   │
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                   │
│  │ Emergency  │  │ Bystander  │  │ Responder  │                   │
│  │  Response  │  │  Guidance  │  │   Stats    │                   │
│  └────────────┘  └────────────┘  └────────────┘                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Geolocation  │  │ Web Speech   │  │ Device Motion│             │
│  │     API      │  │     API      │  │     API      │             │
│  │ (Browser)    │  │ (Browser)    │  │ (Browser)    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Google Maps  │  │   Web Push   │  │  OpenStreet  │             │
│  │  Navigate    │  │   (VAPID)    │  │     Map      │             │
│  │  (Optional)  │  │  Notifications│ │   (Leaflet)  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 SOS Trigger Flow (Step-by-Step)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SOS TRIGGER FLOW                             │
└─────────────────────────────────────────────────────────────────────┘

1. USER CLICKS SOS BUTTON
   │
   ├─→ Modal appears: "Select Emergency Type"
   │   - Medical
   │   - Accident
   │   - Fire
   │   - Personal Safety
   │   - Disaster
   │
2. USER SELECTS TYPE
   │
   ├─→ Browser requests Geolocation permission
   │   - navigator.geolocation.getCurrentPosition()
   │
3. LOCATION CAPTURED (Latitude, Longitude, Accuracy)
   │
   ├─→ User confirms: "TRIGGER SOS"
   │
4. AJAX POST to /emergencies/create/
   │   Payload: {
   │     emergency_type: "medical",
   │     latitude: 12.9716,
   │     longitude: 77.5946,
   │     description: "Chest pain, difficulty breathing"
   │   }
   │
5. BACKEND CREATES EMERGENCY
   │
   ├─→ Emergency.objects.create()
   │   - Generated UUID (emergency_id)
   │   - Status = ACTIVE
   │
   ├─→ calculate_severity() method runs
   │   │
   │   ├─→ Type weight: medical = 30
   │   ├─→ Keywords: "chest pain" +15, "breathing" +15
   │   ├─→ Time score: <5 min old = +10
   │   ├─→ TOTAL: 70 → CRITICAL
   │   │
   │   └─→ severity = "CRITICAL" saved to DB
   │
   ├─→ EmergencyTimeline.objects.create()
   │   - Event: "EMERGENCY_CREATED"
   │   - Actor: victim_user
   │
6. FIND NEARBY RESPONDERS
   │
   ├─→ get_nearby_responders() method
   │   │
   │   ├─→ Query all volunteers within 50km radius
   │   │   WHERE latitude BETWEEN (12.9216, 13.0216)
   │   │   AND longitude BETWEEN (77.5446, 77.6446)
   │   │   AND is_available = True
   │   │   AND verification_status = 'VERIFIED'
   │   │
   │   ├─→ For each responder:
   │   │   - Calculate distance (Haversine formula)
   │   │   - Calculate matching score
   │   │   - Rank by score
   │   │
   │   └─→ Select top 10 responders
   │
7. SEND PUSH NOTIFICATIONS
   │
   ├─→ For each responder:
   │   │
   │   ├─→ Get PushSubscription from DB
   │   │
   │   ├─→ pywebpush.webpush(
   │   │     subscription_info = subscription,
   │   │     data = {
   │   │       "emergency_id": "uuid",
   │   │       "type": "Medical Emergency",
   │   │       "severity": "CRITICAL",
   │   │       "distance": "1.2 km"
   │   │     },
   │   │     vapid_key = VAPID_PRIVATE_KEY
   │   │   )
   │   │
   │   └─→ Browser displays notification
   │       (Even if tab closed!)
   │
8. RESPONDER CLICKS NOTIFICATION
   │
   ├─→ Opens emergency detail page
   │   /emergencies/{emergency_id}/
   │
   ├─→ Sees emergency info:
   │   - Location on map (Leaflet.js)
   │   - Distance (2.3 km)
   │   - Severity badge (red, CRITICAL)
   │   - Description
   │
   ├─→ Clicks "ACCEPT EMERGENCY"
   │
9. BACKEND CREATES EMERGENCY RESPONSE
   │
   ├─→ EmergencyResponse.objects.create()
   │   - emergency = emergency_obj
   │   - responder = volunteer_user
   │   - status = ACCEPTED
   │   - distance_km = 2.3
   │   - estimated_arrival_minutes = 8
   │
   ├─→ Emergency.status = "RESPONDED"
   │
   ├─→ EmergencyTimeline.objects.create()
   │   - Event: "RESPONDER_ACCEPTED"
   │   - Actor: volunteer_user
   │
10. VICTIM SEES UPDATE
    │
    ├─→ Emergency detail page updates
    │   - Status: "Help is on the way!"
    │   - Responder info visible
    │   - ETA countdown timer (7 min 32 sec)
    │
11. RESPONDER LOCATION TRACKING
    │
    ├─→ navigator.geolocation.watchPosition()
    │   - Updates every 10 seconds
    │
    ├─→ POST /api/update-location/
    │   Payload: { lat: 12.9800, lon: 77.6000 }
    │
    ├─→ ResponderLocation.objects.update()
    │
    ├─→ Victim's page re-calculates distance & ETA
    │   - Distance: 1.5 km → 0.8 km → 0.3 km
    │   - ETA: 7 min → 4 min → 2 min
    │
12. RESPONDER ARRIVES
    │
    ├─→ Clicks "I'VE ARRIVED"
    │
    ├─→ EmergencyResponse.status = "ARRIVED"
    │   - actual_arrival_time = now()
    │
    ├─→ EmergencyTimeline.objects.create()
    │   - Event: "RESPONDER_ARRIVED"
    │
13. EMERGENCY RESOLVED
    │
    ├─→ Responder clicks "MARK AS RESOLVED"
    │
    ├─→ Emergency.status = "RESOLVED"
    │
    ├─→ EmergencyResponse.status = "COMPLETED"
    │
    ├─→ Award points & badges to responder
    │   │
    │   ├─→ ResponderStats.total_responses += 1
    │   ├─→ ResponderStats.successful_responses += 1
    │   ├─→ VolunteerProfile.total_points += 80
    │   ├─→ Check badge eligibility
    │   │   - If total_responses == 1: Award "First Responder" badge
    │   │
    │   └─→ Update leaderboard
    │
    └─→ EmergencyTimeline.objects.create()
        - Event: "EMERGENCY_RESOLVED"
        - Actor: volunteer_user

✅ EMERGENCY LIFECYCLE COMPLETE
```

---

## 🤖 Severity Classification Algorithm Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│               RULE-BASED AI SEVERITY CLASSIFICATION                 │
└─────────────────────────────────────────────────────────────────────┘

INPUT: Emergency Object
  {
    emergency_type: "medical",
    description: "Unconscious person, not breathing",
    created_at: "2024-01-15 14:32:00"
  }

STEP 1: Initialize Score
  severity_score = 0

STEP 2: Emergency Type Weight (30-40%)
  ┌──────────────────────────┐
  │ Type Weights:            │
  │ - medical:        30     │
  │ - accident:       25     │
  │ - fire:           35     │
  │ - personal_safety: 20    │
  │ - disaster:       40     │
  └──────────────────────────┘
  
  severity_score += 30  (medical)
  CURRENT SCORE: 30

STEP 3: Keyword Analysis (30%)
  Critical Keywords:
  ┌────────────────────────────┐
  │ "unconscious"     → +15    │
  │ "not breathing"   → +15    │
  │ "chest pain"      → +15    │
  │ "bleeding heavily"→ +15    │
  │ "fire"            → +15    │
  │ "explosion"       → +15    │
  └────────────────────────────┘
  
  Description: "Unconscious person, not breathing"
  - Found "unconscious" → +15
  - Found "not breathing" → +15
  
  severity_score += 30
  CURRENT SCORE: 60

STEP 4: Time Sensitivity (20%)
  age_minutes = (now - created_at).minutes
  age_minutes = 0  (just created)
  
  if age_minutes < 5:
      severity_score += 10
  
  CURRENT SCORE: 70

STEP 5: User History (10%) - FUTURE
  if user.is_new:
      severity_score += 5  (might not describe well)
  
  if user.false_alarm_count > 3:
      severity_score -= 5
  
  CURRENT SCORE: 70 (no change for now)

STEP 6: Contextual Factors - FUTURE
  - Time of day (night = more risky)
  - Location safety score
  - Weather conditions
  
  CURRENT SCORE: 70

STEP 7: Classification
  ┌────────────────────────────┐
  │ if score >= 60: CRITICAL   │
  │ if score >= 40: HIGH       │
  │ if score >= 20: MEDIUM     │
  │ else:           LOW        │
  └────────────────────────────┘
  
  severity_score = 70 → CRITICAL

OUTPUT: severity = "CRITICAL"

VISUAL REPRESENTATION:
  ┌──────────────────────────────────────────────┐
  │  0    10    20    30    40    50    60    70 │
  │  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤│
  │  │ LOW │   MEDIUM  │   HIGH    │  CRITICAL  ││
  │  └─────┴───────────┴───────────┴────────────┘│
  │                                          ▲    │
  │                                        Score  │
  └──────────────────────────────────────────────┘
```

---

## 🎯 Responder Matching Algorithm Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  RESPONDER MATCHING ALGORITHM                       │
└─────────────────────────────────────────────────────────────────────┘

INPUT: Emergency at (12.9716, 77.5946), Type: Medical

STEP 1: Find Volunteers in Radius
  Query: VolunteerProfile.objects.filter(
    is_available = True,
    verification_status = 'VERIFIED',
    user__latitude BETWEEN (12.9216, 13.0216),  # ±0.05° ≈ 50km
    user__longitude BETWEEN (77.5446, 77.6446)
  )
  
  RESULT: 25 volunteers found

STEP 2: Calculate Multi-Factor Score for Each
  
  FOR EACH volunteer IN volunteers:
    
    score = 0
    
    ┌──────────────────────────────────────────┐
    │ FACTOR 1: Distance (50% weight)         │
    └──────────────────────────────────────────┘
    distance = haversine_distance(
      volunteer.location, emergency.location
    )
    
    if distance <= volunteer.availability_radius:
      proximity_ratio = 1 - (distance / volunteer.radius)
      score += proximity_ratio * 50
    
    Example:
    - Volunteer A: 1 km away, radius 5 km
      score += (1 - 1/5) * 50 = 40
    
    - Volunteer B: 4 km away, radius 5 km
      score += (1 - 4/5) * 50 = 10
    
    ┌──────────────────────────────────────────┐
    │ FACTOR 2: Success Rate (20% weight)     │
    └──────────────────────────────────────────┘
    success_rate = successful / total_responses
    score += success_rate * 20
    
    Example:
    - Volunteer A: 18 success / 20 total
      score += 0.9 * 20 = 18
    
    - Volunteer B: 5 success / 10 total
      score += 0.5 * 20 = 10
    
    ┌──────────────────────────────────────────┐
    │ FACTOR 3: Avg Response Time (15% weight)│
    └──────────────────────────────────────────┘
    avg_time = stats.average_response_time_minutes
    
    # Lower time = higher score
    time_score = (10 / max(avg_time, 1)) * 15
    score += time_score
    
    Example:
    - Volunteer A: avg 3 min
      score += (10 / 3) * 15 = 50 (capped at 15)
    
    - Volunteer B: avg 8 min
      score += (10 / 8) * 15 = 18.75 (capped at 15)
    
    ┌──────────────────────────────────────────┐
    │ FACTOR 4: Certification Match (10%)     │
    └──────────────────────────────────────────┘
    if emergency.type == 'medical':
      if certification IN ['PARAMEDIC', 'DOCTOR']:
        score += 10
      elif certification == 'FIRST_AID':
        score += 5
    
    Example:
    - Volunteer A: DOCTOR (medical emergency)
      score += 10
    
    - Volunteer B: FIRST_AID
      score += 5
    
    ┌──────────────────────────────────────────┐
    │ FACTOR 5: Streak Bonus (5% weight)      │
    └──────────────────────────────────────────┘
    streak_bonus = min(current_streak, 10) * 0.5
    score += streak_bonus
    
    Example:
    - Volunteer A: 7-day streak
      score += 7 * 0.5 = 3.5
    
    - Volunteer B: 2-day streak
      score += 2 * 0.5 = 1.0
    
    ┌──────────────────────────────────────────┐
    │ TOTAL SCORE FOR VOLUNTEER A              │
    └──────────────────────────────────────────┘
    Distance:      40.0
    Success Rate:  18.0
    Response Time: 15.0 (max)
    Certification: 10.0
    Streak:         3.5
    ────────────────────
    TOTAL:         86.5

STEP 3: Rank by Score (Descending)
  1. Volunteer A:  86.5 (1.0 km, DOCTOR, 3 min avg, 90% success)
  2. Volunteer C:  78.2 (1.5 km, PARAMEDIC, 4 min avg, 85% success)
  3. Volunteer D:  65.3 (2.0 km, FIRST_AID, 5 min avg, 80% success)
  ...
  10. Volunteer J: 45.1 (4.5 km, FIRST_AID, 7 min avg, 70% success)

STEP 4: Select Top 10
  responders_to_notify = top_10_from_ranked_list

STEP 5: Send Push Notifications
  FOR EACH responder IN responders_to_notify:
    send_push_notification(responder, emergency)

OUTPUT: 10 best-matched volunteers notified

┌────────────────────────────────────────────────────────────────────┐
│                  VISUAL REPRESENTATION                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│            Emergency Location (E)                                 │
│                    ★                                              │
│                 /  |  \                                           │
│              1km  2km  3km                                        │
│             /     |     \                                         │
│           V-A    V-C    V-D                                       │
│           (86)   (78)   (65)                                      │
│                                                                    │
│  V-A: DOCTOR, 1km, 3min avg, 90% success, 7-day streak           │
│  V-C: PARAMEDIC, 1.5km, 4min avg, 85% success, 5-day streak      │
│  V-D: FIRST_AID, 2km, 5min avg, 80% success, 2-day streak        │
│                                                                    │
│  → Top 3 notified immediately                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🕐 Bystander Mode Auto-Activation Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│              BYSTANDER MODE AUTO-ACTIVATION                         │
└─────────────────────────────────────────────────────────────────────┘

TRIGGER: Cron Job (every 1 minute)
  Command: python manage.py activate_bystander_mode

STEP 1: Find Eligible Emergencies
  Query: Emergency.objects.filter(
    status = 'ACTIVE',  # Not yet responded to
    bystander_mode_active = False,
    created_at <= now - timedelta(minutes=5)
  )
  
  Example Result:
  - Emergency #1234: Created 6 minutes ago, no responder

STEP 2: FOR EACH eligible emergency
  
  ┌──────────────────────────────────────────┐
  │ Check Response Status                    │
  └──────────────────────────────────────────┘
  responses = EmergencyResponse.objects.filter(
    emergency = emergency,
    status__in = ['ACCEPTED', 'EN_ROUTE', 'ARRIVED']
  )
  
  if responses.exists():
    # Responder already on the way, skip
    continue
  
  ┌──────────────────────────────────────────┐
  │ Activate Bystander Mode                  │
  └──────────────────────────────────────────┘
  emergency.bystander_mode_active = True
  emergency.save()
  
  ┌──────────────────────────────────────────┐
  │ Create Timeline Event                    │
  └──────────────────────────────────────────┘
  EmergencyTimeline.objects.create(
    emergency = emergency,
    event_type = 'BYSTANDER_MODE_ACTIVATED',
    description = 'No responder arrived within 5 minutes',
    actor = None
  )
  
  ┌──────────────────────────────────────────┐
  │ Send Notification to Victim              │
  └──────────────────────────────────────────┘
  # Future: Push notification
  # "No responder yet. Tap for first-aid guidance."
  
  LOG: "✓ Activated bystander mode for emergency #1234"

STEP 3: Victim Sees Update

  Emergency Detail Page:
  ┌────────────────────────────────────────┐
  │  ⚠️ No Responder Yet                   │
  │                                        │
  │  A trained volunteer hasn't arrived    │
  │  yet. If you or a bystander can help,  │
  │  follow these first-aid instructions.  │
  │                                        │
  │  ┌────────────────────────────────┐   │
  │  │  📋 VIEW FIRST-AID GUIDANCE    │   │
  │  └────────────────────────────────┘   │
  └────────────────────────────────────────┘

STEP 4: User Clicks "View Guidance"

  Redirects to: /emergencies/{id}/bystander/
  
  Loads appropriate guidance based on emergency type:
  - Medical → CPR steps (7 steps)
  - Accident → Bleeding control (7 steps)
  - Fire → Burns treatment (6 steps)
  - Personal Safety → Safety protocol (6 steps)
  - Disaster → Emergency shelter (6 steps)

STEP 5: Interactive Guidance Interface

  ┌────────────────────────────────────────────┐
  │  🚑 First-Aid Guidance: CPR                │
  │                                            │
  │  Progress: Step 3 of 7 [████▒▒▒] 43%      │
  │                                            │
  │  ┌────────────────────────────────────┐   │
  │  │ 3️⃣ Check Breathing                 │   │
  │  │                                    │   │
  │  │ Place your ear near the person's   │   │
  │  │ mouth and nose. Look for chest     │   │
  │  │ movement. Listen for breathing.    │   │
  │  │                                    │   │
  │  │ ⚠️ WARNING: If not breathing or    │   │
  │  │    gasping, begin CPR immediately. │   │
  │  │                                    │   │
  │  │ ┌──────────┐  ┌──────────┐       │   │
  │  │ │ ▶ Listen │  │ ✓ Done   │       │   │
  │  │ └──────────┘  └──────────┘       │   │
  │  └────────────────────────────────────┘   │
  │                                            │
  │  [◄ Previous]            [Next Step ►]    │
  └────────────────────────────────────────────┘

STEP 6: Voice Guidance (Text-to-Speech)

  User clicks "▶ Listen"
  
  JavaScript:
  const utterance = new SpeechSynthesisUtterance(
    "Step 3: Check Breathing. " +
    "Place your ear near the person's mouth and nose. " +
    "Look for chest movement. Listen for breathing. " +
    "Warning: If not breathing or gasping, begin CPR immediately."
  );
  speechSynthesis.speak(utterance);

STEP 7: Progress Tracking

  User clicks "✓ Done"
  
  - Mark step as complete in local storage
  - Update progress bar (57%)
  - Auto-advance to next step

FLOW COMPLETE: Bystander empowered to help while waiting for professionals
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW DIAGRAM                            │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Browser    │
│  (Client)    │
└──────┬───────┘
       │
       │ 1. User Action (Click SOS)
       ▼
┌──────────────────────────┐
│   JavaScript (main.js)   │
│  - Capture location      │
│  - Prepare payload       │
└──────┬───────────────────┘
       │
       │ 2. AJAX POST
       │    /emergencies/create/
       │    { type, lat, lon }
       ▼
┌──────────────────────────┐
│  Django View             │
│  (emergencies/views.py)  │
│  - Validate data         │
│  - Create emergency      │
└──────┬───────────────────┘
       │
       │ 3. Save to DB
       ▼
┌──────────────────────────┐
│   Emergency Model        │
│  - emergency.save()      │
│  - Triggers post_save    │
└──────┬───────────────────┘
       │
       ├──────────────────────┐
       │                      │
       │ 4a. calculate_       │ 4b. get_nearby_
       │     severity()       │     responders()
       ▼                      ▼
┌────────────┐        ┌────────────────┐
│ Severity   │        │ Responder      │
│ Algorithm  │        │ Matching       │
│ (Rule-AI)  │        │ Algorithm      │
└──────┬─────┘        └────┬───────────┘
       │                   │
       │ 5a. Update        │ 5b. Notify
       │     severity      │     volunteers
       ▼                   ▼
┌────────────┐        ┌────────────────┐
│ Database   │        │ Push Service   │
│ (Severity  │        │ (pywebpush)    │
│  = CRITICAL)│        └────┬───────────┘
└────────────┘             │
                           │ 6. Browser Push
                           ▼
                    ┌──────────────┐
                    │ Volunteer's  │
                    │ Browser      │
                    │ (Notification)│
                    └──────┬───────┘
                           │
                           │ 7. Click → Accept
                           ▼
                    ┌──────────────────┐
                    │ Emergency        │
                    │ Response Created │
                    │ status = ACCEPTED│
                    └──────┬───────────┘
                           │
                           │ 8. Update victim
                           ▼
                    ┌──────────────┐
                    │ Victim's     │
                    │ Browser      │
                    │ (Map update, │
                    │  ETA timer)  │
                    └──────────────┘
```

---

## 🎮 Gamification Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GAMIFICATION SYSTEM FLOW                       │
└─────────────────────────────────────────────────────────────────────┘

EVENT: Responder completes emergency
  EmergencyResponse.status = 'COMPLETED'

TRIGGER: Django Signal (post_save)

┌────────────────────────────────────────────────────────────────────┐
│                        AWARD POINTS                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Base Points:              +50                                     │
│  Speed Bonus:              +20 (arrived < 5 min)                   │
│  Severity Bonus:           +10 (CRITICAL emergency)                │
│  Night Shift Bonus:        +15 (10pm - 6am)                        │
│  ──────────────────────────────                                   │
│  TOTAL:                    +95                                     │
│                                                                    │
│  VolunteerProfile.total_points += 95                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                       UPDATE STATISTICS                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ResponderStats.total_responses += 1                               │
│  ResponderStats.successful_responses += 1                          │
│                                                                    │
│  Calculate avg_response_time:                                      │
│    old_avg = 6.2 minutes                                           │
│    this_response = 4.5 minutes                                     │
│    total_responses = 21                                            │
│    new_avg = ((20 * 6.2) + 4.5) / 21 = 6.1 minutes                 │
│                                                                    │
│  ResponderStats.average_response_time_minutes = 6.1                │
│                                                                    │
│  Calculate total_distance:                                         │
│    old_distance = 85.3 km                                          │
│    this_distance = 2.3 km                                          │
│    total_distance = 87.6 km                                        │
│                                                                    │
│  ResponderStats.total_distance_traveled_km = 87.6                  │
│  ResponderStats.lives_impacted += 1                                │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                          UPDATE STREAK                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  last_active = yesterday (2024-01-14)                              │
│  today = 2024-01-15                                                │
│                                                                    │
│  if (today - last_active).days == 1:                               │
│      current_streak += 1  # Consecutive day                        │
│  elif (today - last_active).days > 1:                              │
│      current_streak = 1  # Streak broken                           │
│                                                                    │
│  VolunteerProfile.current_streak_days = 7                          │
│  VolunteerProfile.last_active_date = 2024-01-15                    │
│                                                                    │
│  if current_streak > longest_streak:                               │
│      VolunteerProfile.longest_streak_days = 7                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                       CHECK BADGE ELIGIBILITY                      │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Milestone Badges                                             │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │ IF total_responses == 1:                                     │ │
│  │    ✓ Award "First Responder"                                 │ │
│  │                                                              │ │
│  │ IF total_responses == 10:                                    │ │
│  │    ✓ Award "Dedicated Hero"                                  │ │
│  │                                                              │ │
│  │ IF total_responses == 50:                                    │ │
│  │    □ Award "Elite Responder" (not yet - currently 21)        │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Performance Badges                                           │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │ IF avg_response_time <= 5 AND total_responses >= 5:         │ │
│  │    ✓ Award "Speed Demon" (avg = 6.1, not yet)                │ │
│  │                                                              │ │
│  │ IF success_rate == 1.0 AND total_responses >= 5:            │ │
│  │    ✓ Award "Perfect Record" (21/21 = 100%)                   │ │
│  │    → AWARDED! +100 points bonus                              │ │
│  │                                                              │ │
│  │ IF total_distance >= 100:                                    │ │
│  │    □ Award "Marathon Runner" (87.6 km, not yet)              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Special Badges                                               │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │ IF current_streak >= 7:                                      │ │
│  │    ✓ Award "Week Warrior" (7-day streak!)                    │ │
│  │    → AWARDED! +50 points bonus                               │ │
│  │                                                              │ │
│  │ IF count(responses between 10pm-6am) >= 5:                   │ │
│  │    □ Award "Night Owl" (currently 3)                         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                         AWARD NEW BADGES                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Badges Earned This Response:                                      │
│    1. "Perfect Record" (+100 points)                               │
│    2. "Week Warrior" (+50 points)                                  │
│                                                                    │
│  ResponderStats.badges.add(perfect_record_badge)                   │
│  ResponderStats.badges.add(week_warrior_badge)                     │
│                                                                    │
│  VolunteerProfile.total_points += 150  (badge bonuses)             │
│                                                                    │
│  TOTAL POINTS THIS SESSION: 95 + 150 = 245 points!                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                          LEVEL UP CHECK                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Level Thresholds:                                                 │
│    Level 1: 0-99 points                                            │
│    Level 2: 100-299 points                                         │
│    Level 3: 300-599 points                                         │
│    Level 4: 600-999 points                                         │
│    Level 5: 1000+ points                                           │
│                                                                    │
│  Before: 1,855 points → Level 5                                    │
│  After:  2,100 points → Level 5 (no change)                        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                        UPDATE LEADERBOARD                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Rank  | Volunteer      | Points | Responses | Badges             │
│  ──────────────────────────────────────────────────────────────── │
│    1   | Sarah K        | 2,500  |    35     |  9  ⭐             │
│    2   | John D         | 2,100  |    21     |  6  ⭐ (YOU!)      │
│    3   | Mike R         | 1,950  |    28     |  7                 │
│    4   | Emma L         | 1,800  |    24     |  5                 │
│                                                                    │
│  → Moved up from #3 to #2! 🎉                                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

RESULT: Gamification complete!
  - +245 total points awarded
  - 2 new badges earned
  - Leaderboard rank improved (#3 → #2)
  - Streak continues (7 days)
  - Achievements unlocked notification sent
```

---

**These diagrams should help you explain the system architecture and flows during your CEP exhibition!** 🚀
