from flask import Blueprint, request, jsonify, g
from __init__ import app, db
from api.jwt_authorize import token_required
from model.scoreboard import Scoreboard
from model.user import User

scoreboard_api = Blueprint('scoreboard_api', __name__, url_prefix='/api/scoreboard')

@scoreboard_api.route('/', methods=['GET'])
@token_required()
def get_user_scores():
    """Retrieve all scores for the authenticated user."""
    current_user = g.current_user
    scores = Scoreboard.query.filter_by(uid=current_user._uid).order_by(Scoreboard.timestamp.desc()).all()
    user_scores = [{
        "id": score.id,
        "score": score.score,
        "timestamp": score.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for score in scores]
    return jsonify(user_scores)

@scoreboard_api.route('/', methods=['POST'])
@token_required()
def add_score():
    """Add a new score for the authenticated user."""
    current_user = g.current_user
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    score_value = data.get('score')

    if score_value is None:
        return jsonify({"error": "Missing score"}), 400

    try:
        new_score = Scoreboard(uid=current_user._uid, score=score_value)
        db.session.add(new_score)
        db.session.commit()
        return jsonify({"message": "Score added successfully", "id": new_score.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@scoreboard_api.route('/top', methods=['GET'])
def get_top_scores():
    """Retrieve the top 10 scores across all users."""
    top_scores = Scoreboard.query.order_by(Scoreboard.score.desc()).limit(10).all()
    leaderboard = [{
        "username": User.query.get(score.uid).username if User.query.get(score.uid) else "Unknown",
        "score":    score.score,
        "timestamp": score.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for score in top_scores]

    return jsonify(leaderboard)
