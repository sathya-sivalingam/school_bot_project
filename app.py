from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# The URL where your Rasa server is running
# Default for Rasa is 5005
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def home():
    # Ensure index.html is inside a folder named 'templates'
    return render_template('index.html')

@app.route('/chat', methods=['POST'])

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    if not user_data or "message" not in user_data:
        return jsonify([{"text": "I didn't receive a message."}]), 400

    user_msg = user_data.get("message")
    
    # We use a unique sender ID (like 'user123') so Rasa can 
    # track individual conversations separately.
    payload = {
        "sender": "student_user", 
        "message": user_msg
    }

    try:
        # Timeout added to prevent the Flask app from hanging if Rasa is slow
        response = requests.post(RASA_API_URL, json=payload, timeout=10)
        response.raise_for_status() # Check for HTTP errors (404, 500, etc.)
        
        rasa_response = response.json()
        
        # If Rasa is running but has no answer (Empty Response bug)
        if not rasa_response:
            return jsonify([{"text": "The bot is thinking, but has no answer right now."}])
            
        return jsonify(rasa_response)

    except requests.exceptions.ConnectionError:
        return jsonify([{"text": "Connection Error: Is the Rasa server running on port 5005?"}])
    except Exception as e:
        return jsonify([{"text": f"Error: {str(e)}"}])

if __name__ == '__main__':
    # Using port 8000 to avoid conflict with Rasa (5005) and Action Server (5055)
    app.run(port=8000, debug=True)