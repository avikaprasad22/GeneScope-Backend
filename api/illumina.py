import json
import random
import requests
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from model.illumina import GeneRecord

illumina_api = Blueprint("illumina_api", __name__, url_prefix="/api")
CORS(illumina_api, origins=["http://127.0.0.1:4504"])
api = Api(illumina_api)

# Load local JSON data
with open("mutation_dataset.json") as f:
    mutation_data = json.load(f)

with open("ensembl_sequences.json") as f:
    gene_sequences = json.load(f)

# Pull sequence from Ensembl API (optional fallback, not used in fixed version)
def fetch_sequence_from_ensembl(gene_symbol):
    for organism in ["homo_sapiens", "mus_musculus"]:
        try:
            lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene_symbol}?content-type=application/json"
            response = requests.get(lookup_url, timeout=10)
            if response.status_code != 200 or not response.json():
                continue

            gene_id = response.json()[0]['id']
            seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
            seq_response = requests.get(seq_url, timeout=10)

            if seq_response.status_code == 200:
                return seq_response.text.strip()
        except Exception as e:
            print(f"[WARN] Failed to fetch {gene_symbol}: {e}")
            continue
    return None

# ✅ GET: Choose gene (random or named) and return 12-base sequence + condition
class ChooseGene(Resource):
    def get(self):
        gene_name = request.args.get("name", "random").strip().lower()
        valid_genes = [entry for entry in gene_sequences]
        selected_gene = None

        if gene_name == "random":
            selected_gene = random.choice(valid_genes)
        else:
            for entry in valid_genes:
                if entry["gene"].lower() == gene_name:
                    selected_gene = entry
                    break

        if not selected_gene:
            return jsonify({"error": f"Gene '{gene_name}' not found in sequence data."}), 404

        gene = selected_gene["gene"]
        sequence = selected_gene.get("sequence", "")
        if not sequence or len(sequence) < 12:
            return jsonify({"error": f"Sequence for gene '{gene}' is missing or too short."}), 500

        # Match to mutation data for condition
        condition = "Unknown"
        for record in mutation_data:
            if record["gene"].lower() == gene.lower():
                condition = record.get("condition", "Unknown")
                break

        return jsonify({
            "gene": gene,
            "condition": condition,
            "sequence": sequence[:12]
        })

# ✅ GET: Gene list for dropdown
class GeneList(Resource):
    def get(self):
        try:
            gene_names = sorted({entry["gene"] for entry in gene_sequences})
            return jsonify({"genes": gene_names})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# ✅ POST: Log mutation attempt
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

            attempt = GeneRecord(
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

# ✅ POST: Match a 12-base sequence to known genes
class CheckSequence(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_seq = data.get("sequence", "").upper()

            if len(user_seq) != 12:
                return jsonify({"error": "Sequence must be exactly 12 bases."}), 400

            matched_gene = None
            for entry in gene_sequences:
                full_seq = entry["sequence"].upper()
                for i in range(len(full_seq) - 11):
                    if user_seq == full_seq[i:i+12]:
                        matched_gene = entry["gene"]
                        break
                if matched_gene:
                    break

            if not matched_gene:
                return jsonify({"error": "No gene match found."}), 404

            for record in mutation_data:
                if record["gene"].lower() == matched_gene.lower():
                    return jsonify({
                        "gene": matched_gene,
                        "condition": record.get("condition", "Unknown"),
                        "mutation": "Unknown"
                    })

            return jsonify({
                "gene": matched_gene,
                "condition": "Unknown",
                "mutation": "Unknown"
            })

        except Exception as e:
            print(f"[ERROR] CheckSequence failed: {e}")
            return jsonify({"error": str(e)}), 500

# ✅ Register all endpoints
api.add_resource(ChooseGene, "/choose-gene")
api.add_resource(GeneList, "/gene-list")
api.add_resource(CheckMutation, "/check-mutation")
api.add_resource(CheckSequence, "/check-sequence")