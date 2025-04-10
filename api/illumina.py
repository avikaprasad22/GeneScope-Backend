import json
import random
import requests
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from model.illumina import MutationQuiz  # ✅ Add this for database interaction

illumina_api = Blueprint("illumina_api", __name__, url_prefix="/api")
api = Api(illumina_api)

# Load the preprocessed mutation data
with open("mutation_dataset.json") as f:
    mutation_data = json.load(f)

# Ensembl API gene → sequence fetcher
def fetch_sequence(gene_symbol):
    for organism in ["homo_sapiens", "mus_musculus"]:
        try:
            lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene_symbol}?content-type=application/json"
            response = requests.get(lookup_url)
            if response.status_code != 200 or not response.json():
                continue

            gene_id = response.json()[0]['id']
            seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
            seq_response = requests.get(seq_url)

            if seq_response.status_code == 200:
                return seq_response.text.strip()
        except Exception as e:
            print(f"[WARN] Failed to fetch sequence for {gene_symbol}: {e}")
            continue
    return None

# GET endpoint: fetch a quiz question
class GetSequence(Resource):
    def get(self):
        tries = 0
        max_tries = 20

        while tries < max_tries:
            entry = random.choice(mutation_data)
            gene = entry["gene"]

            sequence = fetch_sequence(gene)
            if sequence:
                short_seq = sequence[:150] + "..." if len(sequence) > 150 else sequence
                return jsonify({
                    "gene": gene,
                    "condition": entry["condition"],
                    "mutation": entry["mutation"],
                    "sequence": short_seq
                })

            tries += 1
            print(f"[INFO] Retry {tries}: sequence not found for gene {gene}")

        return jsonify({"error": "❌ Could not find a gene with both mutation and sequence"}), 500

# POST endpoint: receive guess and log result
class CheckMutation(Resource):
    def post(self):
        try:
            data = request.get_json()
            guess = data.get("guess")
            correct = data.get("correct")
            gene = data.get("gene")
            condition = data.get("condition")
            mutation = data.get("mutation")
            sequence = data.get("sequence")

            is_correct = guess == correct
            message = "✅ Correct!" if is_correct else f"❌ Incorrect. It was a {correct}."

            # Save to the database
            attempt = MutationQuiz(
                gene=gene,
                condition=condition,
                mutation=mutation,
                sequence=sequence,
                correct=is_correct
            )
            attempt.create()

            return jsonify({"message": message})

        except Exception as e:
            return jsonify({"error": f"Failed to save quiz attempt: {str(e)}"}), 500

# Register endpoints
api.add_resource(GetSequence, "/get-sequence")
api.add_resource(CheckMutation, "/check-mutation")
