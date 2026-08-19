console.log("LogStream Extension loaded! Waiting for manual trigger.");

// Change this to the CSS class of the title on your target website
const TARGET_CLASS = '.linetitle3';

// ENVIRONMENT TOGGLE: Uncomment the server you want to use!

// Option 1: V1 Local Development (Ngrok)
const SERVER_URL = 'https://YOUR_NGROK_URL.ngrok-free.app/stream-update';

// Option 2: V2 Production Cloud (PythonAnywhere)
// const SERVER_URL = 'https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com/stream-update';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    
    if (request.action === "log_episode") {
        let htmlElement = document.querySelector(TARGET_CLASS);

        if (htmlElement) {
            let rawTitle = htmlElement.innerText;
            let cleanTitle = rawTitle.replace(/"/g, '').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();

            console.log("Title found:", cleanTitle);

            fetch(SERVER_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: cleanTitle })
            })
            .then(response => {
                if (response.ok) {
                    console.log("Successfully beamed to Python Server!");
                    sendResponse({ status: "success", title: cleanTitle });
                } else {
                    console.error("Server received the request but returned an error.");
                    sendResponse({ status: "error", message: "Server returned an error." });
                }
            })
            .catch(error => {
                console.error("Network Error. Is your active server running?", error);
                sendResponse({ status: "error", message: "Network Error. Server down?" });
            });

            return true; 
        } else {
            console.log("Target class not found on this page. Tracker is sleeping.");
            sendResponse({ status: "error", message: "Could not find anime title on this page." });
        }
    }
});