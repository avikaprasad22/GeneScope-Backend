import pandas as pd
import os

class DatasetLoader:
    """
    Loads the genetic disorders dataset and defines features and questions.
    """

    def __init__(self):
        self.dataset_map = {
            "genetic_disorder": {
                "file": "Training.csv",  # from the Kaggle dataset
                "features": ["Age", "Sex", "Family_History", "Symptom_1", "Symptom_2"],
                "target": "Genetic_Disorder_Present",
                "questions": [
                    ("Age", "What is your age?"),
                    ("Sex", "Sex assigned at birth (male/female):"),
                    ("Family_History", "Do you have a family history of this disorder? (yes/no):"),
                    ("Symptom_1", "Are you experiencing symptom 1 (e.g. fatigue)? (yes/no):"),
                    ("Symptom_2", "Are you experiencing symptom 2 (e.g. joint pain)? (yes/no):"),
                ],
            }
        }

    def load_dataset(self, condition_name):
        key = "genetic_disorder"
        config = self.dataset_map[key]
        path = os.path.join("Training.csv")  # assumes file is in same directory
        df = pd.read_csv(path)
        return df, config["features"], config["target"], config["questions"]
