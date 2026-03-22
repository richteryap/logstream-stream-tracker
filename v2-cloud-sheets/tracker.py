from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import gspread

app = Flask(__name__)
CORS(app)

try:
    gc = gspread.service_account(filename='credentials.json')
    
    db = gc.open("Stream Tracker").sheet1
    print("Successfully connected to Google Sheets!")
except Exception as e:
    print("Google Sheets Connection Failed. Is credentials.json in the folder?", e)

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
        existing_titles = db.col_values(2)
        
        # check duplicate title in the database (Column B)
        if stream_title in existing_titles:
            print("Duplicate title detected in database. Skipping entry.")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            
            # Append a new row to the bottom of the sheet: [Column A, Column B]
            db.append_row([current_time, stream_title])
            print("Successfully saved to Google Sheets!")
            
    except Exception as e:
        print("Failed to push to database:", e)
    # ====================================================
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Python Master Listener is running!")
    app.run(host='0.0.0.0', port=5000)