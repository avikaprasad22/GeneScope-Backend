from flask import Blueprint, request, jsonify
import requests
import random

questions_api = Blueprint('questions', __name__, url_prefix="/api")

# Trivia API Base URL (fetch only 1 question per request)
TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&category=17"

# Cache to store previously fetched questions
cached_questions = []

@questions_api.route('/get_question', methods=['GET'])
def get_question():
    """Fetches a single trivia question with difficulty selection, optimizing response time."""
    global cached_questions
    
    difficulty = request.args.get('difficulty', 'medium')  # Default: medium

    # If cached questions exist, use them instead of making a new API request
    if cached_questions:
        question_data = cached_questions.pop()  # Retrieve a question from cache
    else:
        api_url = f"{TRIVIA_API_URL}&difficulty={difficulty}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            # Validate API response
            if "results" not in data or not data["results"]:
                return jsonify({"error": "No questions found"}), 404

            cached_questions = data["results"]  # Store fetched questions in cache
            question_data = cached_questions.pop()  # Get one question

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to fetch question: {str(e)}"}), 500

    # Shuffle answers
    options = question_data["incorrect_answers"] + [question_data["correct_answer"]]
    random.shuffle(options)

    question = {
        "question": question_data["question"],
        "options": options,
        "correct_answer": question_data["correct_answer"]
    }

    return jsonify(question)
