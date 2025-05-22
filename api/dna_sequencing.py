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
    def fetch_sequence(self, organism, gene_symbol):
        organism = organism.lower().replace(' ', '_')
        gene_symbol = gene_symbol.upper()

        if not organism or not gene_symbol:
            return {"error": "Please provide both 'organism' and 'gene'"}, 400

        lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene_symbol}?content-type=application/json"
        lookup_response = requests.get(lookup_url)

        if lookup_response.status_code != 200 or not lookup_response.json():
            return {"error": f"No gene ID found for {gene_symbol} in {organism}"}, 404

        gene_id = lookup_response.json()[0]['id']
        seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
        seq_response = requests.get(seq_url)

        if seq_response.status_code != 200:
            return {"error": "Failed to fetch sequence from Ensembl"}, 500

        return {
            "gene": gene_symbol,
            "organism": organism,
            "ensembl_id": gene_id,
            "sequence": seq_response.text[:30]  # First 30 characters
        }, 200

    def post(self):
        try:
            print("Sequence POST request received")
            data = request.json
            organism = data.get('organism', '')
            gene_symbol = data.get('gene', '')

            result, status = self.fetch_sequence(organism, gene_symbol)
            response = jsonify(result)
            response.status_code = status

            # Add CORS headers
            response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4504")
            response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Credentials", "true")

            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def get(self):
        try:
            print("Sequence GET request received")
            organism = request.args.get('organism', '')
            gene_symbol = request.args.get('gene', '')

            result, status = self.fetch_sequence(organism, gene_symbol)
            response = jsonify(result)
            response.status_code = status

            # Add CORS headers
            response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4504")
            response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Credentials", "true")

            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

# Register only this
api.add_resource(DNAGene, '/sequence')
