import os
import requests
from flask import request, jsonify, Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Allow frontend requests (adjust the port if needed)
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

# Gene ID mapping for organisms (Ensembl IDs)
GENE_IDS = {
    "human": "ENSG00000139618",        # BRCA2 gene
    "bacteria": "EBMG00000000001",     # Example placeholder
    "virus": "ENSG00000284733",        # Example: viral gene
    "strawberry": "ENSFAG00000000002"  # Placeholder
}

# Define the /sequence POST endpoint
@app.route('/sequence', methods=['POST'])
def get_dna_sequence():
    try:
        print("Sequence request received")
        organism = request.json.get('organism', '').lower()
        if not organism:
            print("No organism provided")
            return jsonify({"error": "No organism provided"}), 400

        gene_id = GENE_IDS.get(organism)
        if not gene_id:
            print(f"Organism '{organism}' not found")
            return jsonify({"error": f"Organism '{organism}' not found"}), 404

        url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
        print(f"Fetching from Ensembl: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching data from Ensembl")
            return jsonify({"error": "Failed to fetch sequence from Ensembl"}), 500

        return jsonify({"sequence": response.text})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8206)
