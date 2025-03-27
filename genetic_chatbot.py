import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from dataset_loader import DatasetLoader

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are a genetics AI assistant. Ask follow-up health questions based on dataset features. "
        "After gathering user input, predict the likelihood of the user having a genetic disorder using machine learning."
    ),
)

def predict_risk(df, features, target, user_input):
    X = df[features].copy()
    y = df[target]

    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = X[col].str.lower().map({'yes': 1, 'no': 0, 'male': 1, 'female': 0})

    model = LogisticRegression()
    model.fit(X, y)

    input_df = pd.DataFrame([user_input])
    for col in input_df.columns:
        if input_df[col].dtype == 'object':
            input_df[col] = input_df[col].str.lower().map({'yes': 1, 'no': 0, 'male': 1, 'female': 0})

    prob = model.predict_proba(input_df[features])[0][1]
    return prob

def main():
    print("\U0001f9ec Welcome to GenePredictor AI!")
    print("I’ll ask a few questions and estimate your genetic disorder risk.\n")

    chat = model.start_chat()
    loader = DatasetLoader()

    chat.send_message("What genetic condition are you concerned about?")
    print("GenePredictor: What genetic condition are you concerned about?")
    _ = input("You: ")  # For now we use the same dataset regardless of condition

    df, features, target, questions = loader.load_dataset("genetic_disorder")

    user_input = {}
    for key, question in questions:
        chat.send_message(question)
        answer = input(f"{question} ")
        user_input[key] = answer

    likelihood = predict_risk(df, features, target, user_input)

    print(f"\n\U0001f4ca Your estimated risk of having the disorder is: {likelihood:.1%}")
    print("\u2757 This is not a medical diagnosis. Please consult a healthcare professional.")

if __name__ == "__main__":
    main()