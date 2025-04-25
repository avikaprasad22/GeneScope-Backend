from flask import Blueprint, jsonify
import requests, random, string

questions_api = Blueprint('questions', __name__, url_prefix="/api")

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

    sampled_records = random.sample(all_records, k=min(20, len(all_records)))  # Sample a variety of records
    questions = []

    for record in sampled_records:
        chrom, symbol, desc, gene_type, gene_id = record
        qtype = random.choice(['chromosome', 'gene_type', 'description', 'gene_id'])

        if qtype == 'chromosome':
            correct_answer = chrom
            options = {chrom}
            options.update(rec[0] for rec in random.sample(all_records, k=10) if rec[0] != chrom)
            options = list(options)[:4]
            question = f"On which chromosome is the gene {symbol} ({desc}) located?"

        elif qtype == 'gene_type':
            correct_answer = gene_type
            options = {gene_type}
            options.update(rec[3] for rec in random.sample(all_records, k=10) if rec[3] != gene_type)
            options = list(options)[:4]
            question = f"What type of gene is {symbol}?"

        elif qtype == 'description':
            correct_answer = desc
            options = {desc}
            options.update(rec[2] for rec in random.sample(all_records, k=10) if rec[2] != desc)
            options = list(options)[:4]
            question = f"Which description best matches the gene {symbol}?"

        else:  # gene_id
            correct_answer = gene_id
            options = {gene_id}
            options.update(rec[4] for rec in random.sample(all_records, k=10) if rec[4] != gene_id)
            options = list(options)[:4]
            question = f"What is the Gene ID for the gene {symbol}?"

        if len(options) < 4:
            continue  # Skip this question if not enough options

        random.shuffle(options)
        questions.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })

        if len(questions) == 10:
            break

    return jsonify(questions)
