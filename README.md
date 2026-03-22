# LogStream

> **A Universal, Cross-Device Media Stream Tracker**

An event-driven, fullstack tracking architecture that scrapes DOM elements and logs them across both desktop and mobile browsers. This project was specifically engineered to bypass native mobile browser extension restrictions (such as those strictly enforced by **Brave Browser on Android**) by utilizing a custom JavaScript bookmarklet payload.

## Technical Highlights
* **Hybrid Deployment:** Supports both **Local Development** (Ngrok tunneling) and **Cloud Production** (PythonAnywhere) environments.
* **Dual-Engine Logging:** Modular backend supports logging to a persistent local `.txt` file or a structured **Google Sheets Database**.
* **Timezone Aware:** Implements `pytz` localization to ensure logs match the user's local time (Asia/Manila) regardless of server location.
* **Cross-Device Architecture:** Bridges the gap between PC extensions and mobile bookmarklets using a unified Flask API.
* **CORS & Security:** Robust handling of preflight `OPTIONS` requests and HTTPS mixed-content policies.

## Tech Stack
* **Backend:** Python 3.13, Flask, Flask-CORS
* **Database:** Google Sheets API (`gspread`), Local File I/O
* **Deployment:** PythonAnywhere, Ngrok (for local testing)
* **Frontend:** Vanilla JavaScript, Chrome Extension MV3, Web Bookmarklets

---

## Configuration

### 1. Targeting Different Sites
LogStream is modular. To target a different streaming platform, update the CSS selector in the frontend scripts:

```javascript
// Default targets elements with class .linetitle3
let htmlElement = document.querySelector('.YOUR_TARGET_CLASS_HERE');
```

### 2. Google Sheets Setup (Cloud Version)

To use the Google Sheets engine:
1. Enable **Google Drive** and **Google Sheets** APIs in the Google Cloud Console.
2. Create a **Service Account**, download the JSON key, and rename it to *credentials.json*.
3. Create a Google Sheet named *Stream Tracker* and share it with the Service Account email as an **Editor**.


---

## Installation & Deployment

### Local Version (Testing)

**1. Prerequisites**
* Python 3.x installed
* A free Ngrok account and Auth Token

**2. Clone & Install dependencies**

```bash
# Activate Python Environment
python -m venv .venv

# Install dependencies
pip install -r requirements.txt
```

**3. Start the Backend Services**
You will need two terminal windows running simultaneously.

**Terminal 1 (The API Receiver):**
Starts the Flask server to listen for incoming payloads on 0.0.0.0.

```bash

# Start the API
python tracker.py
```

**Terminal 2 (The Mobile Tunnel):**
Generates the secure public URL for your mobile device. The --region=ap flag is utilized for optimized low-latency routing in the Asia-Pacific region.

```bash

# Start the tunnel (Asia-Pacific region)
ngrok http 5000 --region=ap
```
*(Copy the generated https://[your-url].ngrok-free.app link for the mobile setup).*

### Cloud Version (PythonAnywhere)

**1. Environment Setup**
* Create a **PythonAnywhere** account.
* On the **Web** tab, click **"Add a new web app"**.
* Select **Flask** and choose **Python 3.13** (or your current version).
* Ensure your project path points to */home/YOUR_USERNAME/mysite/*.

**2. Uploading Project Assets**
Navigate to the **Files** tab on PythonAnywhere and upload your production files into the */mysite/* directory:
* *flask_app.py* (The cloud version of your tracker)
* *credentials.json* (Your Google Service Account key)

**3. Server-Side Dependencies**
You must install your libraries into the PythonAnywhere environment. Open a Bash Console and run:

```bash
# Installs libraries for the specific Python 3.13 environment
pip3.13 install --user flask-cors gspread pytz
```

**4. Going Live**
* Go back to the **Web** tab.
* Click the big green **Reload [your-username].pythonanywhere.com** button.
* Your API is now live at *https://your-username.pythonanywhere.com/stream-update*.

---

## Usage Guide

### Desktop (Chrome/Brave)
1. Navigate to brave://extensions/ or chrome://extensions/.
2. Enable **Developer mode** in the top right.
3. Click **Load unpacked** and select the extension folder in this repository.
4. The extension will automatically detect and log the configured DOM element upon page load.

**Mobile (Brave/Chrome Android)**
Because privacy-focused mobile browsers (like Brave) block standard extensions, this utilizes a custom JS Bookmarklet payload.

1. Create a new bookmark in your mobile browser and name it *Track Stream*.
2. Copy and save this as a bookmark URL. Replace the URL with your PythonAnywhere or Ngrok link:
```javascript
javascript:(function(){let htmlElement=document.querySelector('.linetitle3');if(htmlElement){let rawTitle=htmlElement.innerText;let cleanTitle=rawTitle.replace(/"/g,'').replace(/\n/g,' ').replace(/\s+/g,' ').trim();fetch('https://YOUR_URL.pythonanywhere.com/stream-update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:cleanTitle})}).then(response=>alert("Beamed to database!")).catch(error=>alert("Network Error. Is the server running?"));}else{alert("Title not found.");}})();
```

3. When on the target page, tap the address bar, search for *Track Stream*, and tap the bookmark to securely bridge the payload to your local server.

---
## Author
**Richter Anthony P. Yap**
