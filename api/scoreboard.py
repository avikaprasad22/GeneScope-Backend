from flask import Blueprint, request, jsonify
import json
import os

scoreboard_api = Blueprint('scoreboard', __name__, url_prefix="/api")
SCOREBOARD_FILE = "scoreboard.json"

# Initialize scoreboard file if not exists
if not os.path.exists(SCOREBOARD_FILE):
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump([], f)

@scoreboard_api.route('/submit_scores', methods=['POST'])
def submit_score():
    """Saves user score."""
    data = request.json
    username = data.get("username")
    score = data.get("score")

    if not username or score is None:
        return jsonify({"error": "Missing username or score"}), 400

    with open(SCOREBOARD_FILE, "r") as f:
        scores = json.load(f)

    scores.append({"username": username, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10

    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scores, f)

    return jsonify({"message": "Score saved successfully!"})

@scoreboard_api.route('/get_scores', methods=['GET'])
def get_scores():
    """Retrieves the top 10 scores."""
    with open(SCOREBOARD_FILE, "r") as f:
        scores = json.load(f)
    return jsonify(scores)
