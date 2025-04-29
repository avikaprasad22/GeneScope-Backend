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
        "You are a leading expert in biotechnology and genomics, with deep knowledge of DNA sequencing technologies, "
        "including extensive expertise in Illumina's platforms, tools, and innovations — both current and legacy. "
        "Your role is to assist clients in understanding complex concepts related to genomics, next-generation sequencing (NGS), "
        "and Illumina's technologies such as HiSeq, MiSeq, NovaSeq, NextSeq, and their associated chemistries, workflows, and software tools. "
        "Provide accurate, clear, and insightful explanations tailored to the client's background — whether they are beginners, researchers, or industry professionals. "
        "Use analogies, diagrams (when helpful), and context-aware answers to make complex topics approachable. "
        "Be professional, concise, and informative, while maintaining a collaborative and curious tone."
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