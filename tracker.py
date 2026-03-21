from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) 

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Private-Network'] = 'true'
    return response

@app.route('/stream-update', methods=['POST', 'OPTIONS'])
def receive_update():
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.json
    stream_title = data.get('title', 'Unknown Title')
    
    print(f"Watching \"{stream_title}.\"")
    
    # ====================================================
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        with open("watch_history.txt", "a", encoding="utf-8") as file:
            file.write(f"[{current_time}] {stream_title}\n")
            
        print("Successfully saved to watch_history.txt!")
    except Exception as e:
        print("Failed to save to text file:", e)
    # ====================================================
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Python Master Listener is running!")
    print("Listening on all networks (0.0.0.0) for Desktop and Mobile (Ngrok)...")
    app.run(host='0.0.0.0', port=5000)