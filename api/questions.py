from flask import Blueprint, jsonify, request
import requests, random, string

questions_api = Blueprint('questions_api', __name__, url_prefix="/api")

GENE_API_URL = "https://clinicaltables.nlm.nih.gov/api/ncbi_genes/v3/search"

# Helper to fetch a broad list of gene records
def fetch_gene_records():
    try:
        random_term = random.choice(string.ascii_uppercase)
        params = {
            "terms": random_term,
            "count": 200,
            "df": "chromosome,Symbol,description,type_of_gene,GeneID",
        }
        resp = requests.get(GENE_API_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data[3]
    except Exception as e:
        print(f"[fetch_gene_records] error: {e}")
        return []

@questions_api.route('/get_questions', methods=['GET'])
def get_questions():
    difficulty = request.args.get('difficulty', 'easy').lower()

    if difficulty == 'easy':
        try:
            response = requests.get("https://opentdb.com/api.php?amount=50&category=17&difficulty=easy&type=multiple")
            response.raise_for_status()
            data = response.json()

            if data.get("response_code") != 0 or "results" not in data:
                return jsonify({"error": "Failed to fetch easy questions."}), 500

            questions = []
            for item in data["results"]:
                options = item["incorrect_answers"] + [item["correct_answer"]]
                random.shuffle(options)
                questions.append({
                    "question": item["question"],
                    "options": options,
                    "correct_answer": item["correct_answer"],
                    "difficulty": "easy"
                })

            return jsonify(questions)

        except Exception as e:
            print(f"[get_easy_questions] error: {e}")
            return jsonify({"error": "Unable to retrieve easy questions."}), 500

    # MEDIUM and HARD logic with gene data
    all_records = fetch_gene_records()
    all_records = [r for r in all_records if all(r)]  # Remove incomplete records

    if len(all_records) < 20:
        return jsonify({"error": "Not enough gene data to generate questions."}), 404

    sampled_records = random.sample(all_records, k=min(30, len(all_records)))
    questions = []

    gene_type_descriptions = {
        "protein-coding": "This gene gives instructions to make proteins.",
        "pseudogene": "This gene is like a broken version of a regular gene.",
        "ncRNA": "This gene doesn't make proteins but helps control others.",
        "tRNA": "This gene helps build proteins.",
        "rRNA": "This gene helps the cell's protein factories work.",
        "snRNA": "This gene helps process genetic messages.",
        "miscRNA": "This gene makes RNA with other important jobs.",
        "unknown": "The function of this gene isn't clearly known yet."
    }

    available_gene_types = list(gene_type_descriptions.keys())

    for record in sampled_records:
        chrom, symbol, desc, gene_type, gene_id = record

        if not desc.strip() or len(desc) > 200:
            continue
        if not gene_type.strip() or len(gene_type) > 50:
            continue

        qtype = random.choice(['gene_type', 'description'])

        if qtype == 'gene_type':
            correct_answer = gene_type
            hint = gene_type_descriptions.get(correct_answer, "")

            all_other = [gt for gt in available_gene_types if gt != correct_answer]
            sampled_incorrect = random.sample(all_other, k=min(3, len(all_other)))

            if difficulty == "medium":
                question = f"What type of gene is **{symbol}**?"
            else:
                question = f"Classify the gene **{symbol}** by function."

        elif qtype == 'description':
            correct_answer = desc
            all_other = list(set(
                rec[2] for rec in all_records
                if rec[2] != correct_answer and rec[2] and len(rec[2]) < 200
            ))
            sampled_incorrect = random.sample(all_other, k=min(3, len(all_other)))

            if difficulty == "medium":
                question = f"Which description matches the gene **{symbol}**?"
            else:
                question = f"Provide the functional description of **{symbol}**."

        options = sampled_incorrect + [correct_answer]
        random.shuffle(options)

        questions.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "difficulty": difficulty
        })

    return jsonify(questions)
