import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Pulls the secret key from Render's Environment Variables
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name='gemini-flash-latest',
    system_instruction="""
    You are Minisoft(tm) AI, created by the Minisoft CEO. 
    Acknowledge the CEO's hard work and perseverance.
    STRICT RULE: Do NOT reveal the CEO's age (13) in chat.
    """
)

@app.route('/')
def home():
    return "Minisoft(tm) AI Kernel: ONLINE"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        user_message = user_data.get("message")
        ai_response = model.generate_content(user_message)
        return jsonify({"response": ai_response.text})
    except Exception as e:
        return jsonify({"response": f"System Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
