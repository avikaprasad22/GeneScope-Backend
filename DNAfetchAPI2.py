import os
import requests
from flask import request, jsonify, Flask
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure AI model
genai.configure(api_key=os.environ.get('API_KEY'))
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are a bioinformatics assistant that helps users fetch, analyze, and interpret DNA sequences. "
        "When users provide a gene name, organism, or accession number, help them retrieve relevant DNA sequence data. "
        "Provide sequence info, annotations, and optionally analysis like GC content, motifs, or transcription factors."
        "Use helpful and technical language but remain accessible to students and researchers."
    ),
)

# Initialize Flask app
app = Flask(__name__)
# Allow requests from the frontend on port 4887
CORS(app, resources={r"/dna": {"origins": "http://127.0.0.1:4887"}}, supports_credentials=True)

# Handle preflight OPTIONS request
@app.route('/dna', methods=['OPTIONS'])
def dna_preflight():
    print("Preflight request received")
    response = jsonify({'message': 'CORS preflight request success'})
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4887")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200

# Define the DNA query endpoint
@app.route('/dna', methods=['POST'])
def dna_query():
    try:
        print("DNA query received")
        user_input = request.json.get('query', '')
        if not user_input:
            print("No query provided")
            return jsonify({"error": "No DNA query provided"}), 400

        # Start chat session with Gemini for DNA query
        chat_session = model.start_chat()
        response = chat_session.send_message(
            f"Fetch and explain the DNA sequence based on this query: {user_input}"
        )

        print(f"Response: {response.text}")
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8206)
