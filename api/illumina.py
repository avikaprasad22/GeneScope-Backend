import json
import random
import requests
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

illumina_api = Blueprint("illumina_api", __name__, url_prefix="/api")
api = Api(illumina_api)

# Load preprocessed mutation data
with open("mutation_dataset.json") as f:
    mutation_data = json.load(f)

def fetch_sequence(gene_symbol):
    """Try to fetch DNA sequence for a given gene symbol using Ensembl API"""
    # Try common organisms in order (you can expand this list)
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
                return organism, gene_id, seq_response.text.strip()
        except Exception as e:
            print(f"[WARN] Ensembl fetch failed for {gene_symbol}: {e}")
            continue

    return None, None, None  # No valid sequence found

class GetSequence(Resource):
    def get(self):
        tries = 0
        max_tries = 20

        while tries < max_tries:
            entry = random.choice(mutation_data)
            gene = entry["gene"]

            _, _, sequence = fetch_sequence(gene)
            if sequence:
                short_seq = sequence[:150] + "..." if len(sequence) > 150 else sequence

                return jsonify({
                    "gene": gene,
                    "condition": entry["condition"],
                    "mutation": entry["mutation"],
                    "sequence": short_seq
                })

            tries += 1
            print(f"[INFO] Retry {tries}: no sequence found for {gene}")

        return jsonify({"error": "Could not find a gene with both mutation and sequence data."}), 500

class CheckMutation(Resource):
    def post(self):
        data = request.get_json()
        guess = data.get("guess")
        correct = data.get("correct")

        message = "✅ Correct!" if guess == correct else f"❌ Incorrect. It was a {correct}."
        return jsonify({"message": message})

api.add_resource(GetSequence, "/get-sequence")
api.add_resource(CheckMutation, "/check-mutation")
