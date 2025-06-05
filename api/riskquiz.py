# routes/riskquiz.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS 
from flask_cors import cross_origin
from model.riskquiz import DiseasePredictor

riskquiz_api = Blueprint("riskquiz_api", __name__, url_prefix="/riskquiz")
predictor = DiseasePredictor("symptoms.json")

@riskquiz_api.route("/api/get_symptoms")
@cross_origin(origins="http://127.0.0.1:4504")
def get_symptoms():
    disease = request.args.get("disease", "")
    top_symptoms = predictor.get_symptoms_for_disease(disease)
    if not top_symptoms:
        return jsonify({"success": False, "error": "Disease not found"})
    return jsonify({"success": True, "symptoms": top_symptoms, "matched_disease": disease})

@riskquiz_api.route("/api/predict", methods=["POST"])
@cross_origin(origins="http://127.0.0.1:4504")
def predict():
    data = request.get_json()
    try:
        risk = predictor.predict(data)
        return jsonify({"risk": risk})
    except Exception as e:
        return jsonify({"error": str(e)}), 400