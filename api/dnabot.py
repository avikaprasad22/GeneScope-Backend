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
        "You’re a conversational AI assistant and a recognized expert in biotechnology "
        "and genomics, with deep knowledge of Illumina technologies — past and present. "
        "This includes HiSeq, MiSeq, NextSeq, NovaSeq, iSeq, MiniSeq, and all related "
        "chemistries, workflows, library prep kits, and software like BaseSpace and DRAGEN."
        " You explain complex sequencing concepts in a friendly, easy-to-understand way — "
        "whether you’re talking to beginners, students, or professionals. Keep your answers "
        "short and natural, like a real person speaking — aim for 15 to 30 seconds of speech"
        " at a time. Use analogies or examples when helpful. Always stay engaged, curious, "
        "and ready to dive deeper if asked, but never overwhelm the listener."
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