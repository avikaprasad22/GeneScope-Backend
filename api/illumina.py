import os
import random
import requests
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from dotenv import load_dotenv

load_dotenv()

illumina_api = Blueprint('illumina_api', __name__, url_prefix='/api')
api = Api(illumina_api)

# Sample gene dataset
GENE_LIST = [
    ("homo_sapiens", "BRCA1"),
    ("homo_sapiens", "TP53"),
    ("mus_musculus", "Trp53"),
    ("homo_sapiens", "EGFR"),
    ("homo_sapiens", "MYC"),
    ("homo_sapiens", "PTEN"),
    ("homo_sapiens", "APOE"),
    ("mus_musculus", "Akt1"),
    ("homo_sapiens", "GATA3"),
    ("homo_sapiens", "CDKN2A"),
]

def fetch_random_sequence():
    organism, gene = random.choice(GENE_LIST)
    print(f"[INFO] Selected gene: {gene} from {organism}")

    lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene}?content-type=application/json"
    lookup_response = requests.get(lookup_url)
    if lookup_response.status_code != 200 or not lookup_response.json():
        raise Exception(f"Could not find gene ID for {gene}")

    gene_id = lookup_response.json()[0]['id']
    seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
    seq_response = requests.get(seq_url)
    if seq_response.status_code != 200:
        raise Exception("Failed to fetch sequence")

    return gene, organism, gene_id, seq_response.text.strip()

class GetSequence(Resource):
    def get(self):
        try:
            gene, organism, gene_id, sequence = fetch_random_sequence()
            return jsonify({
                "gene": gene,
                "organism": organism,
                "ensembl_id": gene_id,
                "sequence": sequence,
                "mutation": "none"  # placeholder until you implement real comparison
            })
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return jsonify({"error": f"Failed to fetch gene sequence: {str(e)}"}), 500

class CheckMutation(Resource):
    def post(self):
        data = request.get_json()
        guess = data.get('guess')
        correct = data.get('correct')

        msg = "✅ Correct!" if guess == correct else f"❌ Incorrect. It was a {correct}."
        return jsonify({"message": msg})

# Register endpoints
api.add_resource(GetSequence, '/get-sequence')
api.add_resource(CheckMutation, '/check-mutation')
