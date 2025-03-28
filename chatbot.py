import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from difflib import get_close_matches

class DiseasePredictor:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.symptom_columns = self.df.columns[:-1]
        self.label_column = self.df.columns[-1]
        self.diseases = self.df[self.label_column].unique().tolist()

        # Train the model
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
        input_vector = [symptom_dict.get(symptom, 0) for symptom in self.symptom_columns]
        probabilities = self.model.predict_proba([input_vector])[0]
        disease_index = self.model.classes_.tolist().index(symptom_dict["target_disease"])
        return probabilities[disease_index] * 100

# Conversational chatbot in terminal
if __name__ == "__main__":
    predictor = DiseasePredictor("symbipredict_2024.csv")

    print("🧬 Welcome to SymbiBot! Tell me a disease and I’ll ask about symptoms to estimate your risk.\n")
    print("-" * 60)

    while True:
        disease_input = input("🩺 Disease to check for (or 'exit' to quit): ").strip()
        if disease_input.lower() == "exit":
            print("👋 Goodbye! Stay safe.")
            break

        top_symptoms, matched_disease = predictor.get_symptoms_for_disease(disease_input)
        if not top_symptoms:
            print("⚠️ I couldn’t find a match for that disease. Try a different name.\n")
            continue

        print(f"\n🧠 Great! I found: '{matched_disease}'. Please answer with 'yes' or 'no':\n")
        user_symptoms = {}
        for symptom in top_symptoms:
            ans = input(f"• Do you have '{symptom.replace('_', ' ')}'? ").strip().lower()
            user_symptoms[symptom] = 1 if ans in ["yes", "y"] else 0

        user_symptoms["target_disease"] = matched_disease
        risk = predictor.predict(user_symptoms)

        print(f"\n📊 Likelihood of {matched_disease}: **{risk:.2f}%**\n")
        print("-" * 60)
        if risk > 50:
            print("⚠️ High risk detected! Please consult a healthcare professional.\n")
        else:
            print("😊 Low risk. But always keep an eye on your health!\n")