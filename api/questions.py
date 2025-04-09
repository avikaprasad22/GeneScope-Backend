from flask import Blueprint, request, jsonify
import requests
import random

questions_api = Blueprint('questions', __name__, url_prefix="/api")

# Trivia API Base URL (fetch multiple questions per request)
TRIVIA_API_URL = "https://opentdb.com/api.php?amount=15&category=17"

@questions_api.route('/get_questions', methods=['GET'])
def get_questions():
    """Fetches a batch of trivia questions for preloading."""
    difficulty = request.args.get('difficulty', 'medium')
    api_url = f"{TRIVIA_API_URL}&difficulty={difficulty}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if "results" not in data or not data["results"]:
            return jsonify({"error": "No questions found"}), 404

        questions = []
        for q in data["results"]:
            options = q["incorrect_answers"] + [q["correct_answer"]]
            random.shuffle(options)
            questions.append({
                "question": q["question"],
                "options": options,
                "correct_answer": q["correct_answer"]
            })

        return jsonify(questions)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch questions: {str(e)}"}), 500
