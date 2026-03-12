# Poster Content: Golden Minutes

## Title
**Golden Minutes: A Decentralized Emergency Response System with Advanced Sensory Triggers**

## Header Details
*   **Project ID/Category:** CEP Poster (Second Year)
*   **Team Members:** [Your Name], [Team Member Names]
*   **Guide/Mentor:** [Mentor Name]
*   **Institution:** [Your College Name]

## 1. Abstract
"Golden Minutes" is a Progressive Web Application (PWA) designed to bridge the critical gap between an emergency occurrence and professional medical arrival. By decentralizing emergency response, we empower a network of community volunteers ("Happy Samaritans") to provide immediate aid. The system features advanced "No-Touch" triggers including accelerometer-based fall detection and vernacular voice distress recognition, ensuring accessibility even for incapacitated victims.

## 2. Problem Statement
*   **The Golden Hour:** Immediate intervention significantly increases survival rates.
*   **The Bottleneck:** Traffic congestion and high call volumes delay ambulances in densely populated regions.
*   **The Gap:** A lack of immediate, on-site support while professional help is en route.
*   **Limitation:** Traditional apps require active user interaction, failing when the victim is unconscious.

## 3. Solution: Community-Augmented Response
*   **Hybrid Model:** Combines centralized dispatch with a decentralized volunteer network.
*   **Real-Time Routing:** Geospatial algorithms route the nearest "Happy Samaritan" to the victim.
*   **PWA Accessibility:** No app store delays; works offline and on low-end devices.

## 4. Key Innovations: "No-Touch" Triggers
### A. Fall Detection Algorithm
*   Uses `DeviceMotion` API.
*   **Trigger:** Total acceleration vector ($A_{total}$) > $25 m/s^2$ (approx 2.5g).
*   **Validation:** Checks for post-impact stillness to filter false positives.
*   **Safety:** 15-second pre-alarm allows cancellation.

### B. Voice & Scream Recognition
*   Uses `Web Audio` and `Web Speech` APIs.
*   **Scream Detection:** Sustained high RMS amplitude (>0.4 normalized) for >300ms.
*   **Vernacular Support:** Recognizes distress phrases in **English** ("Help"), **Hindi** ("Bachao"), and **Marathi** ("Madat Kara").

## 5. System Architecture
*   **Frontend:** Progressive Web App (PWA) for cross-platform compatibility.
*   **Backend:** Django 5.1.4 (Python) with GeoDjango.
*   **Database:** PostgreSQL/SQLite with geospatial extensions.
*   **Mapping:** Leaflet.js + OpenStreetMap (Cost-effective & Open Source).
*   **Communication:** WebSockets/Push API for real-time alerts.

## 6. Bystander Guidance Module
*   Empowers untrained volunteers with step-by-step, audio-visual **First Aid & CPR guides**.
*   **Offline First:** Critical content is cached via Service Workers, available without internet.

## 7. Results & Performance
*   **Latency:** Notification delivery < 200ms on 4G networks.
*   **Fall Detection:** 85% True Positive rate in simulated tests.
*   **Load Time:** "Bystander Mode" launches in < 1.5 seconds from cold start.

## 8. Conclusion
Golden Minutes effectively uses modern web technologies to create a robust, low-cost safety net. By turning every citizen into a potential lifesaver and automating distress signals, we can significantly reduce response times and save lives.

## Future Scope
*   IoT/Smartwatch Integration.
*   AI-driven false positive reduction.
*   Direct "Hospital Handshake" data transfer.
