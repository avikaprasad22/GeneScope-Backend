import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from difflib import get_close_matches

class DiseasePredictor:
    def __init__(self, json_file="symptoms.json", csv_file="symbipredict_2024.csv"):
        if not pd.io.common.file_exists(json_file):
            print(f"⚠️ {json_file} not found. Generating from {csv_file}...")
            df = pd.read_csv(csv_file)
            df.to_json(json_file, orient="records")
        self.df = pd.read_json(json_file)

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
        matched_disease = self.match_disease_name(disease_name)
        if not matched_disease:
            return None, None

        filtered_df = self.df[self.df[self.label_column] == matched_disease]
        symptom_sums = filtered_df[self.symptom_columns].sum()
        top_symptoms = symptom_sums[symptom_sums > 0].sort_values(ascending=False).head(10).index.tolist()
        return top_symptoms, matched_disease

    def predict(self, symptom_dict):
        matched_disease = self.match_disease_name(symptom_dict["target_disease"])
        if not matched_disease:
            raise ValueError(f"'{symptom_dict['target_disease']}' not found in known diseases.")

        input_vector = [symptom_dict.get(symptom, 0) for symptom in self.symptom_columns]
        probabilities = self.model.predict_proba([input_vector])[0]
        disease_index = self.model.classes_.tolist().index(matched_disease)
        return probabilities[disease_index] * 100