import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Gemini model config
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
        "You are a health-focused AI assistant. When the user tells you a genetic condition they're concerned about, "
        "use public data (like NIH, WHO, Kaggle) to simulate a dataset with features like age, sex, family history, symptoms, etc. "
        "Then ask 3-5 relevant follow-up questions to estimate risk. You may simulate data if no public dataset is known. "
        "Once you have the answers, return a percentage-based likelihood estimate and a short explanation. "
        "Always clarify this is not a diagnosis."
    ),
)

def simulate_risk_estimate(condition, user_data):
    # Simulate a dataset for the disease (or plug in a real one here)
    # For demo: assume condition with 1,000 people and binary outcome
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "age": np.random.randint(20, 80, size=n),
        "sex": np.random.randint(0, 2, size=n),
        "family_history": np.random.randint(0, 2, size=n),
        "symptoms": np.random.randint(0, 2, size=n),
    })
    # Fake logic: higher risk with older age, male, history, symptoms
    df["has_condition"] = (
        0.01 * df["age"] +
        0.1 * df["sex"] +
        0.2 * df["family_history"] +
        0.25 * df["symptoms"] +
        np.random.normal(0, 0.1, size=n)
    ) > 0.5
    df["has_condition"] = df["has_condition"].astype(int)

    # Train basic model
    features = ["age", "sex", "family_history", "symptoms"]
    model = LogisticRegression()
    model.fit(df[features], df["has_condition"])

    # Convert user inputs to model format
    X_user = pd.DataFrame([user_data])
    X_user["sex"] = 1 if user_data["sex"].lower() == "male" else 0
    X_user["family_history"] = 1 if user_data["family_history"].lower() == "yes" else 0
    X_user["symptoms"] = 1 if user_data["symptoms"].lower() == "yes" else 0
    prob = model.predict_proba(X_user[features])[0][1]
    return prob


def main():
    print("🧬 Welcome to GenePredictor AI")
    print("Let’s estimate your risk based on a genetic condition you're concerned about.\n")

    chat = model.start_chat()

    # Ask user what condition they’re worried about
    condition_prompt = "What genetic condition would you like to inquire about today?"
    print(f"GenePredictor: {condition_prompt}")
    condition = input("You: ").strip()
    chat.send_message(condition_prompt)
    chat.send_message(condition)

    # Ask Gemini to generate relevant follow-up questions
    q_prompt = (
        f"I am concerned about {condition}. Based on what’s known about {condition}, "
        f"please ask me 3-5 short questions about my age, sex, symptoms, family history, or lifestyle that are most relevant to assessing risk."
    )
    follow_up = chat.send_message(q_prompt)
    print(f"\nGenePredictor: {follow_up.text}")

    # Collect user responses
    age = input("Your age: ")
    sex = input("Sex assigned at birth (male/female): ")
    family = input("Do you have a family history? (yes/no): ")
    symptoms = input("Are you experiencing symptoms? (yes/no): ")

    user_data = {
        "age": int(age),
        "sex": sex.lower(),
        "family_history": family.lower(),
        "symptoms": symptoms.lower(),
    }

    # Simulate risk estimate using logic and fake dataset
    risk = simulate_risk_estimate(condition, user_data)

    # Present result
    print(f"\n📊 Based on your answers, your estimated likelihood of having or developing '{condition}' is: {risk:.1%}")
    print("❗ This is not a medical diagnosis. Please consult a healthcare professional for real advice.")

    # Option to go again
    again = input("\nWould you like to assess another condition? (yes/no): ").lower()
    if again == "yes":
        print("\nRestarting...\n")
        main()
    else:
        print("\nThank you for using GenePredictor. Stay healthy!")

if __name__ == "__main__":
    main()