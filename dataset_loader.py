import pandas as pd

class DatasetLoader:
    def __init__(self):
        self.file = "Training.csv"
        self.target = "Disorder Subclass"

    def load_dataset(self, condition_name):
        df = pd.read_csv(self.file)
        df.columns = df.columns.str.strip()

        # Filter rows for this condition
        condition_rows = df[df[self.target].fillna('').str.lower().str.strip() == condition_name.lower().strip()]

        if condition_rows.empty:
            print(f"\n❌ No data found for '{condition_name}'. Check spelling or try another condition.")
            exit()

        # Determine which features are useful (not all NaN or constant)
        candidate_features = [
            col for col in df.columns
            if col not in ["Patient Id", "Patient First Name", "Family Name", "Father's name", "Institute Name",
                           "Location of Institute", "Status", self.target, "Genetic Disorder"]
            and df[col].nunique(dropna=True) > 1
        ]

        # Select top features where condition differs most from others
        top_features = []
        for col in candidate_features:
            if df[col].dtype in ['float64', 'int64']:
                mean_diff = abs(condition_rows[col].mean() - df[col].mean())
                if mean_diff > 0.1:
                    top_features.append((col, mean_diff))
            elif df[col].dtype == 'object':
                val_counts = condition_rows[col].value_counts(normalize=True)
                if any(val_counts > 0.6):
                    top_features.append((col, 1))

        # Sort features by importance and limit to top 6 for simplicity
        top_features = sorted(top_features, key=lambda x: x[1], reverse=True)[:6]
        features = [f[0] for f in top_features]

        # Create questions
        questions = []
        for f in features:
            if "age" in f.lower():
                questions.append((f, "What is your age?"))
            elif "gender" in f.lower() or "sex" in f.lower():
                questions.append((f, "What is your sex assigned at birth? (male/female):"))
            elif "symptom" in f.lower():
                questions.append((f, f"Are you experiencing {f}? (yes/no):"))
            else:
                questions.append((f, f"What is your {f.replace('_', ' ')}? (yes/no or a number):"))

        return df, features, self.target, questions