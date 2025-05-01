from flask import Blueprint, request, jsonify
import pandas as pd
import os

# Blueprint for college API
college_api = Blueprint('college_api', __name__, url_prefix="/api")

def load_dataset():
    """Load the college dataset from a local CSV file."""
    try:
        csv_file = os.path.join(os.path.dirname(__file__), "top_colleges_2022.csv")
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

@college_api.route('/get_colleges', methods=['GET'])
def get_colleges():
    df = load_dataset()
    if df is None:
        return jsonify({"error": "Dataset not found"}), 500

    # Get user preferences
    region = request.args.get("region")
    college_type = request.args.get("college_type")
    setting = request.args.get("campus_setting")
    size = request.args.get("size")
    research = request.args.get("research")

    # Apply direct filters
    if region:
        df = df[df["region"].str.lower() == region.lower()]
    if college_type:
        df = df[df["collegeType"].str.lower() == college_type.lower()]
    if setting:
        df = df[df["campusSetting"].str.lower() == setting.lower()]

    # Apply size filter using totalStudentPop
    if size:
        size = size.lower()
        if size == "small":
            df = df[df["totalStudentPop"] < 5000]
        elif size == "medium":
            df = df[(df["totalStudentPop"] >= 5000) & (df["totalStudentPop"] <= 15000)]
        elif size == "large":
            df = df[df["totalStudentPop"] > 15000]

    # Apply research filter using carnegieClassification
    if research:
        research = research.lower()
        if research == "yes":
            df = df[df["carnegieClassification"].str.contains("high research", case=False, na=False)]
        elif research == "no":
            df = df[~df["carnegieClassification"].str.contains("high research", case=False, na=False)]

    # Return up to 10 matching colleges
    results = df.head(10)

    return jsonify({
        "colleges": results[[
            "organizationName", "description", "state", "city",
            "campusSetting", "collegeType", "region", "website"
        ]].to_dict(orient="records")
    })