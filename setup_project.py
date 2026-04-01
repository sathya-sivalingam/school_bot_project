import os

# Define the folder structure and file contents
files = {
    "actions/actions.py": """
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3

class ActionFetchAttendance(Action):
    def name(self) -> Text:
        return "action_fetch_attendance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        student_id = tracker.get_slot("student_id")
        user_pin = tracker.get_slot("student_pin")

        if not student_id or not user_pin:
            dispatcher.utter_message(text="Please provide both your Student ID and PIN.")
            return []

        try:
            conn = sqlite3.connect('school_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, attendance_percentage FROM student_attendance WHERE student_id=? AND pin=?", (student_id, user_pin))
            result = cursor.fetchone()
            conn.close()

            if result:
                dispatcher.utter_message(text=f"Verified. {result[0]}, your attendance is {result[1]}%.")
            else:
                dispatcher.utter_message(text="Authentication failed. Check your ID and PIN.")
        except Exception as e:
            dispatcher.utter_message(text="Error connecting to database.")
            
        return [SlotSet("student_pin", None)]
""",
    "app.py": """
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    try:
        r = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"sender": "user", "message": user_msg})
        return jsonify(r.json())
    except Exception as e:
        return jsonify([{"text": "Rasa server is not running."}])

if __name__ == '__main__':
    app.run(port=8000, debug=True)
""",
    "endpoints.yml": "action_endpoint:\n  url: 'http://localhost:5055/webhook'",
    "setup_db.py": """
import sqlite3
conn = sqlite3.connect('school_database.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS student_attendance (student_id TEXT, name TEXT, attendance_percentage REAL, pin TEXT)')
c.execute("DELETE FROM student_attendance")
c.execute("INSERT INTO student_attendance VALUES ('S101', 'Alice', 92.5, '1234')")
conn.commit()
conn.close()
print('Database Created!')
"""
}

# Create folders and files
for path, content in files.items():
    directory = os.path.dirname(path)
    
    # FIXED: Only create directory if 'directory' is not an empty string
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(path, "w") as f:
        f.write(content.strip())

print("✅ Project files created successfully without errors!")