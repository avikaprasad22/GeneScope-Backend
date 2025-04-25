from flask import Blueprint, request, jsonify
from model.chatbot import DiseasePredictor

# Define Flask blueprint
chatbot_api = Blueprint("chatbot_api", __name__, url_prefix="/chatbot")

# Load model from JSON
predictor = DiseasePredictor("symptoms.json")

@chatbot_api.route("/get_symptoms")
def get_symptoms():
    disease = request.args.get("disease", "")
    top_symptoms, matched_disease = predictor.get_symptoms_for_disease(disease)
    if not top_symptoms:
        return jsonify({"success": False, "error": "Disease not found"})
    return jsonify({"success": True, "symptoms": top_symptoms, "matched_disease": matched_disease})

@chatbot_api.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        risk = predictor.predict(data)
        return jsonify({"risk": risk})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
