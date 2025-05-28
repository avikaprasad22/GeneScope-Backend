# dna_api.py

import os
import requests
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Blueprint
dna_api = Blueprint('dna_api', __name__, url_prefix='/api')
api = Api(dna_api)

# Correct CORS: allow frontend at 4504 to access everything under /api
CORS(dna_api, resources={r"/*": {"origins": "http://127.0.0.1:4504"}}, supports_credentials=True)

class DNAGene(Resource):
    def post(self):
        try:
            print("Sequence request received")
            data = request.json
            organism = data.get('organism', '').lower().replace(' ', '_')
            gene_symbol = data.get('gene', '').upper()

            if not organism or not gene_symbol:
                return jsonify({"error": "Please provide both 'organism' and 'gene'"}), 400

            # Lookup Ensembl gene ID
            lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene_symbol}?content-type=application/json"
            lookup_response = requests.get(lookup_url)

            if lookup_response.status_code != 200 or not lookup_response.json():
                return jsonify({"error": f"No gene ID found for {gene_symbol} in {organism}"}), 404

            gene_id = lookup_response.json()[0]['id']
            seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
            seq_response = requests.get(seq_url)

            if seq_response.status_code != 200:
                return jsonify({"error": "Failed to fetch sequence from Ensembl"}), 500

            # Prepare the response with sequence data (return only the first 30 characters)
            response = jsonify({
                "gene": gene_symbol,
                "organism": organism,
                "ensembl_id": gene_id,
                "sequence": seq_response.text[:30]  # Only first 30 characters
            })

            # Add CORS headers to the response
            response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4504")
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

@dna_api.route('/genes', methods=['GET'])
def get_gene_list():
    # Ideally, you'd fetch this from a DB or file
    gene_list = [
        {"gene": "ESR1", "organism": "Danio rerio"},
        {"gene": "FOXP2", "organism": "Pan troglodytes"},
        {"gene": "MDR1", "organism": "Canis lupus familiaris"},
        {"gene": "SHH", "organism": "Gallus gallus"},
        {"gene": "CSN2", "organism": "Bos taurus"},  
    ]
    return jsonify(gene_list)

# Register only this
api.add_resource(DNAGene, '/sequence', 'genes')
