# api/giftbot.py

import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get('API_KEY'))

generation_config = {
    "temperature": 1.15,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert in suggesting gifts for people. Your task is to engage "
        "in conversations about gift-giving and provide thoughtful suggestions. "
        "Understand the user's preferences, occasion, and budget to offer personalized "
        "gift ideas. Use relatable examples, humor, and creativity to make the interaction enjoyable."
    ),
)

# Flask Blueprint
dnabot_api = Blueprint('dnabot_api', __name__, url_prefix='/dnabot')

@dnabot_api.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    chat_session = model.start_chat()
    response = chat_session.send_message(user_input)
    return jsonify({"response": response.text})