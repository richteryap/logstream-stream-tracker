from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import gspread
import pytz
import re

app = Flask(__name__)
CORS(app)

TIMEZONE = pytz.timezone('Asia/Manila')

def parse_anime_details(full_title):
    match = re.search(r"(.*)\s+Episode\s+(\d+)", full_title, re.IGNORECASE)
    if match:
        show_name = match.group(1).strip()
        episode_num = int(match.group(2))
        return show_name, episode_num
    return full_title, 0

@app.route('/stream-update', methods=['POST'])
@cross_origin()
def receive_update():
    # Use get_json(silent=True) so empty OPTIONS requests don't crash it
    data = request.get_json(silent=True) or {}
    stream_title = data.get('title', 'Unknown Title')

    show_name, new_ep = parse_anime_details(stream_title)
    print(f"Watching: \"{stream_title}\"")
    
    try:
        # Connect INSIDE the route to prevent server timeouts
        gc = gspread.service_account(filename='credentials.json')
        spreadsheet = gc.open("Stream Tracker")
        
        log_sheet = spreadsheet.sheet1
        library_sheet = spreadsheet.worksheet("Sheet2")
        
        utc_now = datetime.now(pytz.utc)
        time_now = utc_now.astimezone(TIMEZONE)
        current_time = time_now.strftime("%Y-%m-%d %I:%M %p")
        
        # Duplicate Check for Sheet 1
        existing_titles = log_sheet.col_values(2)
        if stream_title in existing_titles:
            print(f"Duplicate title in history. Skipping log: {stream_title}")
        else:
            log_sheet.append_row([current_time, stream_title])
            print(f"Saved to History: {stream_title}")

        # Library Update for Sheet 2
        cell = library_sheet.find(show_name)
        
        if cell is None:
            next_row = len(library_sheet.col_values(1)) + 1
            formula = f'=IF(E{next_row}="", "Watching", IF(B{next_row}>=E{next_row}, "Completed", "Watching"))'

            print(f"Adding new show to Library: {show_name}")

            library_sheet.append_row([show_name, new_ep, current_time, formula], value_input_option='USER_ENTERED')
        else:
            row_index = cell.row
            current_val = library_sheet.cell(row_index, 2).value
            current_ep = int(current_val) if (current_val and str(current_val).isdigit()) else 0

            if new_ep > current_ep:
                library_sheet.update(values=[[new_ep, current_time]], range_name=f"B{row_index}:C{row_index}")
                print(f"Updated Library: {show_name} to Ep {new_ep}")
            else:
                print(f"Library up to date for: {show_name}")
            
    except Exception as e:
        print("Server/Database Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Python Master Listener is running!")
    app.run()