from __init__ import db, app
from datetime import datetime
import random
import logging

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
        
        # Sample questions to add to the database
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
        "question": "Which of the following is an example of personalized medicine?",
        "option_a": "A drug prescribed to all patients with a certain disease",
        "option_b": "Tailoring treatments based on a person's genetic makeup",
        "option_c": "Using a universal vaccine for all individuals",
        "option_d": "Treating everyone with the same dosage of a drug",
        "correct_answer": "Tailoring treatments based on a person's genetic makeup",
        "difficulty": "medium",
        "category": "Personalized Medicine"
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
        "question": "What does the term 'genome' refer to?",
        "option_a": "A group of cells in the body",
        "option_b": "The complete set of genes in an organism",
        "option_c": "The process of protein synthesis",
        "option_d": "A type of mutation in the DNA sequence",
        "correct_answer": "The complete set of genes in an organism",
        "difficulty": "easy",
        "category": "Genetics"
    },
    {
        "question": "What does 'Next-Generation Sequencing' (NGS) allow scientists to do?",
        "option_a": "Analyze the structure of proteins",
        "option_b": "Sequence an individual's entire genome rapidly",
        "option_c": "Manipulate individual DNA sequences in real-time",
        "option_d": "Create genetically modified organisms",
        "correct_answer": "Sequence an individual's entire genome rapidly",
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
        "question": "What is the main ethical concern with gene editing in humans?",
        "option_a": "It can lead to genetic mutations",
        "option_b": "It may be used for non-medical purposes, such as enhancing traits",
        "option_c": "It can cause irreversible changes to the environment",
        "option_d": "It can cure all diseases immediately",
        "correct_answer": "It may be used for non-medical purposes, such as enhancing traits",
        "difficulty": "hard",
        "category": "Bioethics"
    },
    {
        "question": "What is the primary purpose of gene therapy?",
        "option_a": "To treat cancer",
        "option_b": "To replace defective genes with functional ones",
        "option_c": "To improve athletic performance",
        "option_d": "To create genetically modified foods",
        "correct_answer": "To replace defective genes with functional ones",
        "difficulty": "medium",
        "category": "Genetic Research"
    },
    {
        "question": "What does a DNA sequencing machine do?",
        "option_a": "It replicates the DNA",
        "option_b": "It maps the order of nucleotides in DNA",
        "option_c": "It edits DNA sequences",
        "option_d": "It breaks down DNA molecules into smaller fragments",
        "correct_answer": "It maps the order of nucleotides in DNA",
        "difficulty": "easy",
        "category": "DNA Technology"
    },
    {
        "question": "What is a potential application of synthetic biology?",
        "option_a": "Creating new antibiotics to combat resistant bacteria",
        "option_b": "Developing new forms of renewable energy",
        "option_c": "Designing crops that are immune to pests",
        "option_d": "All of the above",
        "correct_answer": "All of the above",
        "difficulty": "medium",
        "category": "Biotechnology"
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
