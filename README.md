# LogStream

> A Universal Web-to-Local Media Stream Tracker

An event-driven, fullstack tracking architecture that automatically scrapes DOM elements (like currently watched media titles) and logs them across both desktop and locked-down mobile web browsers.

This project was specifically engineered to bypass native mobile browser extension restrictions (such as those strictly enforced by **Brave Browser on Android**) by utilizing a custom JavaScript bookmarklet payload. It routes DOM data through a secure Ngrok tunneling bridge directly to a local Python Flask API.

## Technical Highlights
* **Configurable DOM Scraping:** Uses custom, modular JavaScript to parse the DOM. It can be easily configured to target specific CSS classes on any modern streaming platform.
* **Cross-Device Tracking:** Works seamlessly across PC desktop browsers (via Chrome Extension) and restricted mobile browsers like Brave Android (via Bookmarklet Injection).
* **CORS & Security Bypass:** Implements custom Flask headers to handle preflight `OPTIONS` requests, bridging the gap between public HTTPS sites and local HTTP networks.
* **Secure Mobile Tunneling:** Leverages Ngrok to create a secure `HTTPS` tunnel, bypassing mobile mixed-content blocking policies.
* **Indestructible Local Logging:** Appends scraped payloads and timestamps directly to a local `.txt` file for persistent, API-independent storage.

## Tech Stack
* **Backend:** Python, Flask, Flask-CORS
* **Network & Tunneling:** pyngrok, Windows SSH
* **Frontend/Injection:** Vanilla JavaScript, Chrome Extension Manifest V3, Web Bookmarklets
* **Data Storage:** Local Text/Log Parsing


---

## Configuration (Targeting Different Sites)
This scraper is built to be modular. Out of the box, it targets elements with the `.linetitle3` class. 

To configure the tracker for a different streaming site, simply update the CSS selector in the frontend scripts:
```javascript
// Change this line in both content.js and your mobile bookmarklet
let htmlElement = document.querySelector('.YOUR_TARGET_CLASS_HERE');
```


---

## Installation & Setup

**1. Prerequisites**
* Python 3.x installed
* A free Ngrok account and Auth Token

**2. Clone & Install dependencies**
```bash
git clone [https://github.com/richteryap/logstream-stream-tracker.git](https://github.com/richteryap/logstream-stream-tracker.git)
cd logstream-stream-tracker
python -m venv .venv
pip install -r requirements.txt
```

**3. Start the Backend Services**
You will need two terminal windows running simultaneously.

**Terminal 1 (The API Receiver):**
Starts the Flask server to listen for incoming payloads on 0.0.0.0.

```bash
python tracker.py
```

**Terminal 2 (The Mobile Tunnel):**
Generates the secure public URL for your mobile device. The --region=ap flag is utilized for optimized low-latency routing in the Asia-Pacific region.

```bash
ngrok http 5000 --region=ap
```
*(Copy the generated https://[your-url].ngrok-free.app link for the mobile setup).*


---

## Usage Guide

**Desktop (Chrome/Brave)**
1. Navigate to brave://extensions/ or chrome://extensions/.
2. Enable **Developer mode** in the top right.
3. Click **Load unpacked** and select the extension folder in this repository.
4. The extension will automatically detect and log the configured DOM element upon page load.

**Mobile (Brave/Chrome Android)**
Because privacy-focused mobile browsers (like Brave) block standard extensions, this utilizes a custom JS Bookmarklet payload.

1. Create a new bookmark in your mobile browser and name it *Track Stream*.
2. Edit the bookmark and paste the following JavaScript payload into the URL field, replacing the placeholder with your active Ngrok URL:

```javascript
javascript:(function(){let htmlElement=document.querySelector('.linetitle3');if(htmlElement){let rawTitle=htmlElement.innerText;let cleanTitle=rawTitle.replace(/"/g,'').replace(/\n/g,' ').replace(/\s+/g,' ').trim();fetch('https://YOUR_NGROK_URL_HERE.ngrok-free.app/anime-update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:cleanTitle})}).then(response=>alert("Beamed through Ngrok to PC!")).catch(error=>alert("Network Error. Is Python running?"));}else{alert("Title not found.");}})();
```

3. When on the target page, tap the address bar, search for *Track Stream*, and tap the bookmark to securely bridge the payload to your local server.
