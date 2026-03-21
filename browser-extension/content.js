console.log("LogStream Extension is active! Searching for title...");

// Scans the page every 2 seconds (2000ms)
let checkExist = setInterval(function() {
    let htmlElement = document.querySelector('.linetitle3');
    
    // If element finally exists on the page...
    if (htmlElement) {
        clearInterval(checkExist); // Turn off the interval to stop scanning
        
        let rawTitle = htmlElement.innerText;
        let cleanTitle = rawTitle.replace(/"/g, '').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
        console.log("EXTENSION FOUND TITLE:", cleanTitle);

        // Beam it to Python
        fetch('http://127.0.0.1:5000/stream-update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: cleanTitle })
        })
        .then(response => console.log("EXTENSION SENT TO PYTHON!"))
        .catch(error => console.error("NETWORK BLOCK:", error));
    }
}, 2000);