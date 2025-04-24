from flask import Blueprint, jsonify
import requests, random

questions_api = Blueprint('questions', __name__, url_prefix="/api")

GENE_API_URL = "https://clinicaltables.nlm.nih.gov/api/ncbi_genes/v3/search"
GENE_TERMS    = ["APOE", "CFTR", "HBB", "KRAS", "EGFR", "MYC", "TP53", "BRCA1", "TNF", "FMR1"]

def fetch_gene_data(term):
    params = {
        "terms": term,
        "df":    "chromosome,Symbol,description",  # display fields
        "count": 1,
    }
    try:
        resp = requests.get(GENE_API_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        # data[3] is list of display‐field rows
        rows = data[3]
        if not rows:
            return None
        chrom, symbol, desc = rows[0]
        return symbol, chrom, desc
    except Exception as e:
        print(f"[fetch_gene_data] error: {e}")
        return None

def generate_question_format(symbol, chromosome, description):
    # Expanded set of templates for greater variety
    templates = [
        f"Which chromosome houses the {description} gene ({symbol})?",
        f"On which chromosome is {symbol} (\"{description}\") found?",
        f"{symbol} — {description} — is located on which chromosome?",
        f"Which chromosome contains the gene known as {symbol}?",
        f"Select the chromosome number for the gene {symbol}:",
        f"True or False: the gene {symbol} is on chromosome {chromosome}.",
        f"What number chromosome contains the gene {symbol}?",
        f"Fill in the blank: {symbol} is found on chromosome ___.",
        f"{description} ({symbol}) can be found on which human chromosome?",
        f"The gene {symbol}, which codes for {description}, lives on chromosome ____."
    ]
    return random.choice(templates)

@questions_api.route('/get_questions', methods=['GET'])
def get_questions():
    questions = []
    for term in GENE_TERMS:
        info = fetch_gene_data(term)
        if not info:
            continue
        symbol, chrom, desc = info
        qtext = generate_question_format(symbol, chrom, desc)

        # Build four options
        opts = [chrom]
        while len(opts) < 4:
            cand = random.choice([*map(str, range(1, 23)), "X", "Y"])
            if cand not in opts:
                opts.append(cand)
        random.shuffle(opts)

        questions.append({
            "question":       qtext,
            "options":        opts,
            "correct_answer": chrom
        })

    if not questions:
        return jsonify({"error": "No gene questions could be generated."}), 404

    return jsonify(questions)
