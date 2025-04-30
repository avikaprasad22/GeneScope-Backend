import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from difflib import get_close_matches

class DiseasePredictor:
    def __init__(self, json_file):
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File '{json_file}' not found.")

        try:
            self.df = pd.read_json(json_file, orient="records")
        except Exception as e:
            raise ValueError(f"Error loading JSON file: {e}")

        if self.df.empty:
            raise ValueError("Loaded DataFrame is empty.")

        self.symptom_columns = self.df.columns[:-1]
        self.label_column = self.df.columns[-1]
        self.diseases = self.df[self.label_column].unique().tolist()

        self.model = RandomForestClassifier()
        self.model.fit(self.df[self.symptom_columns], self.df[self.label_column])

    def match_disease_name(self, user_input):
        matches = get_close_matches(user_input.lower(), [d.lower() for d in self.diseases], n=1, cutoff=0.4)
        if matches:
            for disease in self.diseases:
                if disease.lower() == matches[0]:
                    return disease
        return None

    def get_symptoms_for_disease(self, disease_name):
        matched = self.match_disease_name(disease_name)
        if not matched:
            return []

        subset = self.df[self.df[self.label_column].str.lower() == matched.lower()]
        if subset.empty:
            return []

        # Compute frequency of each symptom being 1 in rows of this disease
        symptom_counts = subset[self.symptom_columns].sum().sort_values(ascending=False)
        return symptom_counts[symptom_counts > 0].index.tolist()

    def predict(self, symptom_dict):
        symptoms = [symptom_dict.get(col, 0) for col in self.symptom_columns]
        probabilities = self.model.predict_proba([symptoms])[0]

        target_disease = symptom_dict.get("target_disease", "").lower()
        for i, cls in enumerate(self.model.classes_):
            if cls.lower() == target_disease:
                return round(probabilities[i] * 100, 2)

        return 0.0
