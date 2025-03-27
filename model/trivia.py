from __init__ import db, app
from datetime import datetime, date  # Import date explicitly
import random
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the TriviaQuestion model
class TriviaQuestion(db.Model):
    __tablename__ = 'trivia_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    option_a = db.Column(db.String, nullable=False)
    option_b = db.Column(db.String, nullable=False)
    option_c = db.Column(db.String, nullable=False)
    option_d = db.Column(db.String, nullable=False)
    correct_answer = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default='medium')
    category = db.Column(db.String, nullable=False)
    date_added = db.Column(db.Date, default=lambda: datetime.utcnow().date())

    def __repr__(self):
        return f"<TriviaQuestion(id={self.id}, question={self.question}, category={self.category})>"

# Define the TriviaResponse model
class TriviaResponse(db.Model):
    __tablename__ = 'trivia_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('trivia_questions.id'), nullable=False)
    selected_answer = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    question = db.relationship('TriviaQuestion', backref='responses', lazy=True)
    
    def __repr__(self):
        return f"<TriviaResponse(name={self.name}, question_id={self.question_id}, is_correct={self.is_correct}, score={self.score})>"

# Function to initialize the tables and add sample questions
def init_trivia():
    with app.app_context():
        db.create_all()

        # Expanded set of trivia questions
        sample_questions = [
            {
                "question": "What is the main function of CRISPR in gene editing?",
                "option_a": "To create artificial proteins",
                "option_b": "To edit specific DNA sequences",
                "option_c": "To synthesize RNA",
                "option_d": "To prevent gene mutations",
                "correct_answer": "To edit specific DNA sequences",
                "difficulty": "hard",
                "category": "Gene Editing"
            },
            {
                "question": "Which company is known for pioneering gene therapy treatments?",
                "option_a": "Illumina",
                "option_b": "Gilead Sciences",
                "option_c": "Bluebird Bio",
                "option_d": "Amgen",
                "correct_answer": "Bluebird Bio",
                "difficulty": "medium",
                "category": "Genetic Therapy"
            },
            {
                "question": "Which company developed the first widely used next-generation sequencing (NGS) platform?",
                "option_a": "Illumina",
                "option_b": "Thermo Fisher Scientific",
                "option_c": "Oxford Nanopore",
                "option_d": "PacBio",
                "correct_answer": "Illumina",
                "difficulty": "medium",
                "category": "Genomics"
            },
            {
                "question": "Which genetic sequencing technology is commonly used by Illumina?",
                "option_a": "Sanger sequencing",
                "option_b": "Pyrosequencing",
                "option_c": "SBS (Sequencing by Synthesis)",
                "option_d": "Nanopore sequencing",
                "correct_answer": "SBS (Sequencing by Synthesis)",
                "difficulty": "hard",
                "category": "Genomics"
            },
            {
                "question": "Which breakthrough technology was used to sequence the first human genome?",
                "option_a": "Sanger sequencing",
                "option_b": "Nanopore sequencing",
                "option_c": "Illumina sequencing",
                "option_d": "CRISPR sequencing",
                "correct_answer": "Sanger sequencing",
                "difficulty": "medium",
                "category": "Genomics"
            },
            {
                "question": "Which genetic disorder is most commonly tested using newborn screening?",
                "option_a": "Cystic fibrosis",
                "option_b": "Huntington’s disease",
                "option_c": "Sickle cell anemia",
                "option_d": "Both A and C",
                "correct_answer": "Both A and C",
                "difficulty": "easy",
                "category": "Genetic Screening"
            },
            {
                "question": "What is the name of the first FDA-approved gene therapy for cancer?",
                "option_a": "Kymriah",
                "option_b": "Opdivo",
                "option_c": "Herceptin",
                "option_d": "Keytruda",
                "correct_answer": "Kymriah",
                "difficulty": "hard",
                "category": "Cancer Genomics"
            },
            {
                "question": "Which gene is most commonly associated with breast cancer risk?",
                "option_a": "TP53",
                "option_b": "BRCA1",
                "option_c": "MYC",
                "option_d": "KRAS",
                "correct_answer": "BRCA1",
                "difficulty": "medium",
                "category": "Cancer Genomics"
            },
            {
                "question": "What is a key advantage of whole-genome sequencing (WGS) over whole-exome sequencing (WES)?",
                "option_a": "It is cheaper",
                "option_b": "It only sequences protein-coding regions",
                "option_c": "It provides a complete genetic blueprint",
                "option_d": "It is more error-prone",
                "correct_answer": "It provides a complete genetic blueprint",
                "difficulty": "hard",
                "category": "Genomic Research"
            },
            {
                "question": "Which of the following genetic testing services is NOT owned by Illumina?",
                "option_a": "Verifi Prenatal Test",
                "option_b": "23andMe",
                "option_c": "TruSight Oncology",
                "option_d": "NovaSeq",
                "correct_answer": "23andMe",
                "difficulty": "medium",
                "category": "Genomic Companies"
            },
            {
                "question": "Which of the following is a key benefit of personalized medicine?",
                "option_a": "It ensures every patient receives the same treatment",
                "option_b": "It tailors treatments based on an individual’s genetic makeup",
                "option_c": "It eliminates the need for medication",
                "option_d": "It removes all risk of disease",
                "correct_answer": "It tailors treatments based on an individual’s genetic makeup",
                "difficulty": "easy",
                "category": "Personalized Medicine"
            },
            {
                "question": "Illumina sequencing is widely used in cancer research to:",
                "option_a": "Identify genetic mutations linked to cancer",
                "option_b": "Develop new chemotherapy drugs",
                "option_c": "Perform radiation therapy",
                "option_d": "Eliminate cancer cells directly",
                "correct_answer": "Identify genetic mutations linked to cancer",
                "difficulty": "medium",
                "category": "Cancer Genomics"
            },
            {
                "question": "Which part of the DNA is commonly analyzed for ancestry testing?",
                "option_a": "Mitochondrial DNA",
                "option_b": "Y-chromosome DNA",
                "option_c": "Autosomal DNA",
                "option_d": "All of the above",
                "correct_answer": "All of the above",
                "difficulty": "medium",
                "category": "Genetic Ancestry"
            },
            {
                "question": "What is a major challenge in gene therapy?",
                "option_a": "The immune system may reject modified genes",
                "option_b": "Genes cannot be changed in the human body",
                "option_c": "It is not FDA approved",
                "option_d": "It only works on bacteria",
                "correct_answer": "The immune system may reject modified genes",
                "difficulty": "hard",
                "category": "Gene Therapy"
            },
            {
                "question": "How has Illumina contributed to the fight against COVID-19?",
                "option_a": "Developing antiviral drugs",
                "option_b": "Creating mRNA vaccines",
                "option_c": "Sequencing the SARS-CoV-2 virus genome",
                "option_d": "Building ventilators",
                "correct_answer": "Sequencing the SARS-CoV-2 virus genome",
                "difficulty": "hard",
                "category": "Pandemic Research"
            }
        ]

        # Add sample questions to the trivia_questions table
        for question_data in sample_questions:
            question = TriviaQuestion(
                question=question_data['question'],
                option_a=question_data['option_a'],
                option_b=question_data['option_b'],
                option_c=question_data['option_c'],
                option_d=question_data['option_d'],
                correct_answer=question_data['correct_answer'],
                difficulty=question_data['difficulty'],
                category=question_data['category'],
            )
            db.session.add(question)

        # Commit changes to the database
        db.session.commit()
        print("Trivia tables initialized and sample questions added.")

def backup_trivia_data(directory='backup'):
    """Backup trivia questions and responses to JSON files."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Backup trivia questions
    questions = []
    for q in TriviaQuestion.query.all():
        question_dict = q.__dict__.copy()
        question_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
        if isinstance(question_dict.get('date_added'), date):  # Use date from datetime
            question_dict['date_added'] = question_dict['date_added'].isoformat()  # Convert date to string
        questions.append(question_dict)
    
    with open(os.path.join(directory, 'trivia_questions.json'), 'w') as f:
        json.dump(questions, f)
    
    # Backup trivia responses
    responses = []
    for r in TriviaResponse.query.all():
        response_dict = r.__dict__.copy()
        response_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
        responses.append(response_dict)
    
    with open(os.path.join(directory, 'trivia_responses.json'), 'w') as f:
        json.dump(responses, f)
    
    print(f"Trivia data backed up to {directory} directory.")

def restore_trivia_data(directory='backup'):
    """Restore trivia questions and responses from JSON files."""
    # Restore trivia questions
    with open(os.path.join(directory, 'trivia_questions.json'), 'r') as f:
        questions = json.load(f)
        for question_data in questions:
            # Convert date_added back to a date object if it's a string
            if isinstance(question_data.get('date_added'), str):
                question_data['date_added'] = date.fromisoformat(question_data['date_added'])
            question = TriviaQuestion(**question_data)
            db.session.merge(question)
    
    # Restore trivia responses
    with open(os.path.join(directory, 'trivia_responses.json'), 'r') as f:
        responses = json.load(f)
        for response_data in responses:
            response = TriviaResponse(**response_data)
            db.session.merge(response)
    
    db.session.commit()
    print("Trivia data restored from backup.")
