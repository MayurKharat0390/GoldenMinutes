# How to Publish Golden Minutes on Google Play Store

## Phase 1: Preparation (Done!)
I have already configured your Django app as a **PWA (Progressive Web App)**.
- `manifest.json` is ready.
- Service Worker is linked.

### 🔴 Critical Requirement: Deployment
Before you can build the Android App, your website **MUST BE LIVE** on the internet (e.g., `https://goldenminutes.railway.app`).
You CANNOT publish `http://127.0.0.1:8000` to the Play Store.

### 🎨 Design Requirement
You need to create App Icons and save them in `static/images/`:
1.  `icon-192.png` (192x192 pixels)
2.  `icon-512.png` (512x512 pixels)
3.  **Deploy these changes** to your live server.

---

## Phase 2: Build the Android App (TWA)
We will use **Bubblewrap**, Google's official tool for converting PWAs to Android Apps.

### 1. Install Bubblewrap
Open your terminal (PowerShell or CMD) and run:
```bash
npm install -g @bubblewrap/cli
```
*(Requires Node.js installed)*

### 2. Initialize the Project
Create a new folder somewhere on your PC (e.g., `GM_Android_App`), go inside, and run:
```bash
bubblewrap init --manifest https://YOUR-LIVE-SITE-URL.com/static/manifest.json
```
*Replace `YOUR-LIVE-SITE-URL.com` with your actual domain.*

### 3. Answer the Prompts
Bubblewrap will ask you questions. Defaults are usually fine, but ensure:
- **Application Name**: Golden Minutes
- **Start URL**: /

### 4. Build the App
```bash
bubblewrap build
```
This will generate two files:
- `app-release-bundle.aab` (Upload this to Play Store)
- `app-release-apk.apk` (For testing on your phone)

---

## Phase 3: Upload to Play Store

1.  Go to **Google Play Console** (play.google.com/console).
2.  Create a standard developer account ($25 fee).
3.  Click **Create App**.
4.  Upload the `.aab` file you generated.
5.  Fill in the Listing Details (Description, Screenshots, Privacy Policy).
6.  Submit for Review!

### 💡 Pro Tip
Since `Golden Minutes` uses **Location** and **Notifications**:
- In the Play Console "App Content" section, you must declare that you use Location Permissions.
- Explain clearly: *"Location is used to connect emergency responders with nearby victims."*

---
*Good Luck! - AntiGravity*
