from flask import Blueprint, request, jsonify
import pandas as pd
import os
import random

# Blueprint for matching API
matching_api = Blueprint('matching_api', __name__, url_prefix="/api")

# Load the CSV once at the start
csv_path = os.path.join(os.path.dirname(__file__), 'matching_game.csv')
df = pd.read_csv(csv_path)

@matching_api.route('/pairs', methods=['GET'])
def get_pairs():
    difficulty = request.args.get('level', 'beginner').lower()

    if difficulty not in ['beginner', 'intermediate', 'advanced']:
        return jsonify({'error': 'Invalid difficulty level'}), 400

    # Filter terms by difficulty
    filtered = df[df['difficulty'] == difficulty]

    if filtered.empty:
        return jsonify({'error': 'No terms available for this level'}), 404

    # Shuffle and select 8 random pairs (or fewer if not enough)
    pairs = filtered.sample(frac=1).head(min(8, len(filtered))).to_dict(orient='records')

    return jsonify(pairs)
