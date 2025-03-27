import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from dataset_loader import DatasetLoader

# Load Gemini API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Gemini config
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

def predict_risk(df, features, target, user_input, condition):
    X = df[features].copy()
    y = df[target]

    # Drop rows with missing target values
    valid_rows = y.notna()
    X = X[valid_rows]
    y = y[valid_rows]

    # Encode target as binary (1 = condition, 0 = other)
    y = y.astype(str).str.lower().str.strip()
    y = y.apply(lambda val: 1 if val == condition.lower().strip() else 0)

    if y.nunique() < 2:
        print("\n❌ Not enough variety in the dataset to model this condition. Try another.")
        exit()

    # Encode features
    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = X[col].str.lower().map({'yes': 1, 'no': 0, 'male': 1, 'female': 0})

    X = X.fillna(X.median(numeric_only=True)).fillna(0)

    # Split data to compute accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Accuracy
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Prepare user input
    input_df = pd.DataFrame([user_input])
    for col in input_df.columns:
        if input_df[col].dtype == 'object':
            input_df[col] = input_df[col].str.lower().map({'yes': 1, 'no': 0, 'male': 1, 'female': 0})

    input_df = input_df.fillna(0)
    prob = model.predict_proba(input_df[features])[0][1]

    return prob, acc

def main():
    print("\U0001f9ec Welcome to GenePredictor AI!")
    print("I’ll ask a few questions and estimate your genetic disorder risk.\n")

    chat = model.start_chat()
    loader = DatasetLoader()

    print("GenePredictor: What genetic condition are you concerned about?")
    condition = input("You: ")

    df, features, target, questions = loader.load_dataset(condition)

    user_input = {}
    for key, question in questions:
        answer = input(f"{question} ")
        user_input[key] = answer

    likelihood, accuracy = predict_risk(df, features, target, user_input, condition)

    print(f"\n\U0001f4ca Your estimated risk of having {condition.title()} is: {likelihood:.1%}")
    print("\u2757 This is not a medical diagnosis. Please consult a healthcare professional.")

    # Gemini follow-up
    response = chat.send_message(
        f"The user's answers are: {user_input}. The estimated risk of {condition} is {likelihood:.1%}. "
        "Please give simple wellness advice or next steps they can consider."
    )
    print("\nGenePredictor AI Advice:", response.text)

    # Developer-only accuracy comment
    print(f"\n# Model accuracy on internal test split: {accuracy:.2%}")

if __name__ == "__main__":
    main()