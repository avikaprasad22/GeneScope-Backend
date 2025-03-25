from flask import Blueprint, jsonify, request
from __init__ import db, app
from model.trivia import TriviaQuestion, TriviaResponse

# Create a Blueprint for the trivia API
trivia_api = Blueprint('trivia_api', __name__, url_prefix='/api/trivia')

# Route to get a random trivia question
@trivia_api.route('/question', methods=['GET'])
def get_random_question():
    """Retrieve a random trivia question."""
    question = TriviaQuestion.query.order_by(db.func.random()).first()
    if question:
        return jsonify({
            'id': question.id,
            'question': question.question,
            'options': {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d
            },
            'category': question.category,
            'difficulty': question.difficulty
        })
    return jsonify({'error': 'No questions available'}), 404

# Route to submit an answer
@trivia_api.route('/answer', methods=['POST'])
def submit_answer():
    """Submit an answer to a trivia question."""
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        question_id = data.get('question_id')
        selected_answer = data.get('selected_answer')
        
        question = TriviaQuestion.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        is_correct = (selected_answer == question.correct_answer)
        score = 10 if is_correct else 0
        
        response = TriviaResponse(
            name=name,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            score=score
        )
        
        db.session.add(response)
        db.session.commit()
        
        return jsonify({'message': 'Answer submitted', 'correct': is_correct, 'score': score})
    
    return jsonify({'error': 'Request must be JSON'}), 415

# Route to get a user's total score
@trivia_api.route('/score/<string:name>', methods=['GET'])
def get_user_score(name):
    """Retrieve the total score of a user."""
    total_score = db.session.query(db.func.sum(TriviaResponse.score)).filter_by(name=name).scalar()
    return jsonify({'name': name, 'total_score': total_score or 0})

# Route to add a trivia question
@trivia_api.route('/question', methods=['POST'])
def add_trivia_question():
    """Add a new trivia question to the database."""
    if request.is_json:
        data = request.get_json()
        
        # Get data from the request
        question_text = data.get('question')
        option_a = data.get('option_a')
        option_b = data.get('option_b')
        option_c = data.get('option_c')
        option_d = data.get('option_d')
        correct_answer = data.get('correct_answer')
        difficulty = data.get('difficulty', 'medium')  # Default to 'medium' if not provided
        category = data.get('category')
        
        if not all([question_text, option_a, option_b, option_c, option_d, correct_answer, category]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create and add the new trivia question to the database
        new_question = TriviaQuestion(
            question=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            difficulty=difficulty,
            category=category
        )
        
        db.session.add(new_question)
        db.session.commit()
        
        return jsonify({'message': 'Trivia question added successfully', 'question_id': new_question.id}), 201
    
    return jsonify({'error': 'Request must be JSON'}), 415

# Route to get the leaderboard
@trivia_api.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Retrieve the leaderboard with users and their total scores."""
    leaderboard = (
        db.session.query(
            TriviaResponse.name,
            db.func.sum(TriviaResponse.score).label('total_score')
        )
        .group_by(TriviaResponse.name)
        .order_by(db.desc('total_score'))
        .limit(10)  # Limit to top 10 users
        .all()
    )
    
    return jsonify([
        {'name': entry.name, 'total_score': entry.total_score}
        for entry in leaderboard
    ])
