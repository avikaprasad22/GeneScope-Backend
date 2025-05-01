from flask import Blueprint, jsonify
import requests, random, string

questions_api = Blueprint('questions_api', __name__, url_prefix="/api")

GENE_API_URL = "https://clinicaltables.nlm.nih.gov/api/ncbi_genes/v3/search"

# Helper to fetch a broad list of gene records
def fetch_gene_records():
    try:
        random_term = random.choice(string.ascii_uppercase)  # Random letter for broader gene variety
        params = {
            "terms": random_term,  # Using a random letter to increase variety
            "count": 200,          # Fetch more records to diversify the pool
            "df": "chromosome,Symbol,description,type_of_gene,GeneID",
        }
        resp = requests.get(GENE_API_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data[3]  # This is the list of display-field rows
    except Exception as e:
        print(f"[fetch_gene_records] error: {e}")
        return []

@questions_api.route('/get_questions', methods=['GET'])
def get_questions():
    all_records = fetch_gene_records()
    all_records = [r for r in all_records if all(r)]  # Remove incomplete records

    if len(all_records) < 20:
        return jsonify({"error": "Not enough gene data to generate questions."}), 404

    sampled_records = random.sample(all_records, k=min(20, len(all_records)))
    questions = []

    for record in sampled_records:
        chrom, symbol, desc, gene_type, gene_id = record
        qtype = random.choice(['chromosome', 'gene_type', 'description'])

        # For chromosome-based questions
        if qtype == 'chromosome':
            correct_answer = chrom
            # Focus on the location without raw numbers
            chrom_description = f"Located on {chrom}" if chrom.isdigit() else f"Chromosome {chrom}"
            all_other = list(set(rec[0] for rec in all_records if rec[0] != correct_answer))
            sampled_incorrect = random.sample(all_other, k=min(3, len(all_other)))
            question = f"Where is the gene {symbol} located?"

        # For gene type questions
        elif qtype == 'gene_type':
            correct_answer = gene_type
            gene_type_descriptions = {
                "protein-coding": "This gene makes proteins that your body uses.",
                "pseudogene": "This gene is a 'broken' gene and doesn't make a useful protein.",
                "ncRNA": "This gene doesn't make proteins, but helps control other genes.",
                "tRNA": "This gene helps in the production of proteins in your body.",
                "rRNA": "This gene helps make proteins in the ribosome, the cell's protein factory.",
                "snRNA": "This gene is involved in the processing of other RNA.",
                "miscRNA": "This gene makes RNA with various roles in the cell."
            }
            gene_type_desc = gene_type_descriptions.get(correct_answer, "A gene with a specific role in the cell.")
            all_other = list(set(rec[3] for rec in all_records if rec[3] != correct_answer))
            sampled_incorrect = random.sample(all_other, k=min(3, len(all_other)))
            question = f"What type of gene is {symbol}? (Hint: {gene_type_desc})"

        # For description-based questions
        elif qtype == 'description':
            correct_answer = desc
            # Simplified descriptions for easier understanding
            all_other = list(set(rec[2] for rec in all_records if rec[2] != correct_answer))
            sampled_incorrect = random.sample(all_other, k=min(3, len(all_other)))
            question = f"Which of these best describes the gene {symbol}?"

        options = sampled_incorrect + [correct_answer]
        random.shuffle(options)

        questions.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })

        if len(questions) == 10:
            break

    return jsonify(questions)
