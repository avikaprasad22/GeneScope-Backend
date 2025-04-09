from flask import Blueprint, request, jsonify
import pandas as pd
import os  # ✅ Keep this to work with file paths

# Create Blueprint for handling resource requests
resource_api = Blueprint('resource_api', __name__, url_prefix="/api")

# ✅ Modified: Load local CSV instead of Kaggle
def load_dataset():
    """Loads the student-scores dataset from local CSV file."""
    try:
        csv_file = os.path.join(os.path.dirname(__file__), "student-scores.csv")
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None
    
@resource_api.route('/get_careers', methods=['GET'])
def get_careers_by_biology_score():
    df = load_dataset()
    if df is None:
        return jsonify({"error": "Dataset not found"}), 500

    if "biology_score" not in df.columns or "career_aspiration" not in df.columns:
        return jsonify({"error": "Required columns missing in dataset"}), 500

    df = df[df["biology_score"].notnull()]
    
    target_score = request.args.get("biology_score", type=float)

    if target_score is not None:
        df["score_diff"] = (df["biology_score"] - target_score).abs()
        min_diff = df["score_diff"].min()
        closest_matches = df[df["score_diff"] == min_diff]
    else:
        # 🧠 If no score, just return first 5 careers
        closest_matches = df.head(5)

    return jsonify({
        "careers": closest_matches[["career_aspiration", "biology_score"]].to_dict(orient="records")
    })
