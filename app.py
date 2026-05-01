import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Allows your GitHub Pages terminal to talk to this server

# Load your secrets from Render Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SECRET_PHRASE = os.environ.get("SECRET_PHRASE")

# Configure the Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Use the latest 2026 stable model: Gemini 2.5 Flash
# This replaces the retired gemini-pro and gemini-1.5 models
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def home():
    return "Minisoft(tm) Kernel: ONLINE"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # Generate response from the new Gemini kernel
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        # Returns a professional kernel error if the connection fails
        return jsonify({"response": f"KERNEL ERROR: {str(e)}"}), 500

@app.route('/verify-secret', methods=['POST'])
def verify_secret():
    try:
        data = request.json
        user_input = data.get("secret", "")
        
        # Security handshake with the CEO's secret phrase
        if user_input == SECRET_PHRASE:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render automatically sets the PORT variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
