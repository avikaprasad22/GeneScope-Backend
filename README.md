# Biotechnology Education Platform (Illumina-Aligned)

An interactive website designed for students and educators to explore biotechnology, genetics, and DNA sequencing. Built as a resource to support AP Computer Science Principles, Data Structures, and Biology classes using real-world tools and datasets modeled after Illumina’s genomic technologies.

# For educaters and leaners

This project can be used to:
- Demonstrate biotechnology concepts interactively
- Integrate biology and computer science curricula
- Enable students to explore DNA sequences, mutation types, and gene function hands-on
- Foster inquiry-based learning through visual tools and interactive simulations

---

## Educational Features

- Hands-on **gene mutation simulation** using real DNA sequences.
- Select from Sandbox or Fix-the-Gene game modes.
- Interactive tutorial guides walk users through genetic concepts.
- Connects biology and computer science in a tangible way.
- Designed for classroom integration or independent learning.

---

## Live Site + GitHub

- **Frontend repo:** [Frontend](avikaprasad22.github.io/genescope/)
- **Backend repo:** [Backend](avikaprasad22.github.io/genescope_backend)

---

## Integrated Datasets

This project uses real and simulated data from the following sources:

- [Ensembl REST API](https://rest.ensembl.org) — for accessing live gene sequences.
- [National Institutes of Health (NIH)](https://www.ncbi.nlm.nih.gov/clinvar/) — mutation data from ClinVar.
- [Kaggle Disease Dataset](https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset) — symptom-based disease prediction.
- [NCBI Genetic Database](https://www.ncbi.nlm.nih.gov/) — for genetic research reference.
- [Open Trivia Database](https://opentdb.com/) — for quiz features and practice.

---

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: Jinja2, Tailwind CSS, HTML, JavaScript
- **Database**: SQLite3 (with preloaded `.db` files)
- **APIs**: Ensembl, OpenTDB, NIH/NCBI (via JSON)
- **Deployment**: Docker, docker-compose, AWS, NGINX

---

## Acknowledgments

- Developed for the Open Coding Society
- Entered into the pilot city **Illumina Interactive Biotech Education Game** project
- Dataset and science design inspired by Illumina, NIH, NCBI, and Kaggle

- JWT login and user auth by Aiden Wu, CSP Contributor

---

## License
MIT License
© 2025 Nora Ahadian, Sonika Denuva, Katherine Chen, Zoe He, Avika Prasad, Gabriela Connelly

---

## Project Setup

### 1. clone and install

```bash
mkdir -p ~/biotech-edu && cd ~/biotech-edu
git clone https://github.com/nighthawkcoders/flask_2025.git
cd flask_2025
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. run the app
flask run

### 3. a .env file in your backend
#### containing these user defaults
ADMIN_USER= "toby"
ADMIN_PASSWORD= "123Toby!"
DEFAULT_USER= "hop"
DEFAULT_PASSWORD= "123Hop!"

### 4. Generate your own gemini api key labeled:
API_KEY

### 5. Initialize the database
./scripts/db_init.py
