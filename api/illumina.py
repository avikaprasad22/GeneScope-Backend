import json
import random
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

illumina_api = Blueprint("illumina_api", __name__, url_prefix="/api")
api = Api(illumina_api)

# Load preprocessed mutation data
with open("mutation_dataset.json") as f:
    mutation_data = json.load(f)

class GetSequence(Resource):
    def get(self):
        entry = random.choice(mutation_data)
        return jsonify({
            "gene": entry["gene"],
            "mutation": entry["mutation"],
            "condition": entry["condition"]
        })

class CheckMutation(Resource):
    def post(self):
        data = request.get_json()
        guess = data.get("guess")
        correct = data.get("correct")

        message = "✅ Correct!" if guess == correct else f"❌ Incorrect. It was a {correct}."
        return jsonify({"message": message})

api.add_resource(GetSequence, "/get-sequence")
api.add_resource(CheckMutation, "/check-mutation")