import os
import requests
from flask import request, jsonify, Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/sequence": {"origins": "http://127.0.0.1:3000"}}, supports_credentials=True)

# Handle preflight OPTIONS request
@app.route('/sequence', methods=['OPTIONS'])
def sequence_preflight():
    print("Preflight request received")
    response = jsonify({'message': 'CORS preflight request success'})
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:3000")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200

# Define the dynamic /sequence POST endpoint
@app.route('/sequence', methods=['POST'])
def get_dna_sequence():
    try:
        print("Sequence request received")
        data = request.json
        organism = data.get('organism', '').lower().replace(' ', '_')  # e.g., homo sapiens → homo_sapiens
        gene_symbol = data.get('gene', '').upper()

        if not organism or not gene_symbol:
            return jsonify({"error": "Please provide both 'organism' and 'gene'"}), 400

        # Lookup Ensembl gene ID dynamically
        lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene_symbol}?content-type=application/json"
        print(f"Looking up gene ID from: {lookup_url}")
        lookup_response = requests.get(lookup_url)

        if lookup_response.status_code != 200 or not lookup_response.json():
            return jsonify({"error": f"No gene ID found for {gene_symbol} in {organism}"}), 404

        gene_id = lookup_response.json()[0]['id']
        print(f"Found gene ID: {gene_id}")

        # Now fetch the actual sequence
        seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
        print(f"Fetching sequence from: {seq_url}")
        seq_response = requests.get(seq_url)

        if seq_response.status_code != 200:
            return jsonify({"error": "Failed to fetch sequence from Ensembl"}), 500

        return jsonify({
            "gene": gene_symbol,
            "organism": organism,
            "ensembl_id": gene_id,
            "sequence": seq_response.text
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8206)
