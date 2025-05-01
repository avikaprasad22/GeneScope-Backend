from __init__ import db, app
from sqlalchemy.exc import IntegrityError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of allowed chromosomes
ALLOWED_CHROMOSOMES = [str(i) for i in range(1, 23)] + ["X", "Y", "MT"]

# Define the GeneResource model
class GeneResource(db.Model):
    __tablename__ = 'gene_resources'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    chromosome = db.Column(db.String)
    chromosome_info = db.Column(db.String)  # New
    gene_type = db.Column(db.String)
    gene_type_info = db.Column(db.String)   # New
    gene_id = db.Column(db.String)

    def __repr__(self):
        return f"<GeneResource(symbol={self.symbol}, chromosome={self.chromosome})>"

    def read(self):
        return {
            "symbol": self.symbol,
            "description": self.description,
            "chromosome": self.chromosome,
            "chromosome_info": self.chromosome_info,
            "gene_type": self.gene_type,
            "gene_type_info": self.gene_type_info,
            "gene_id": self.gene_id
        }

# Function to add a new gene resource
def add_gene_resource(symbol, description, chromosome, gene_type, gene_id):
    with app.app_context():
        if chromosome not in ALLOWED_CHROMOSOMES:
            return f"Skipping chromosome {chromosome}: not in allowed list."

        # Friendly gene type info
        gene_type_explanation = {
            "protein-coding": "This gene provides instructions for making a protein.",
            "pseudogene": "A gene that looks like a real one but doesn't produce a functional product.",
            "ncRNA": "Produces non-coding RNA, which can regulate other genes.",
            "tRNA": "Makes transfer RNA that helps build proteins.",
            "rRNA": "Makes ribosomal RNA, part of protein-building ribosomes.",
            "snRNA": "Involved in RNA splicing and processing.",
            "miscRNA": "Produces other RNAs with unique functions."
        }
        gene_type_info = gene_type_explanation.get(gene_type.lower(), "Has a unique role in the cell.")

        chromosome_info = (
            f"Located on Chromosome {chromosome}, involved in essential biological traits."
            if chromosome in ALLOWED_CHROMOSOMES
            else "Chromosome information not clearly defined."
        )

        try:
            new_resource = GeneResource(
                symbol=symbol,
                description=description,
                chromosome=chromosome,
                chromosome_info=chromosome_info,
                gene_type=gene_type,
                gene_type_info=gene_type_info,
                gene_id=gene_id
            )
            db.session.add(new_resource)
            db.session.commit()
            return f"GeneResource {symbol} added successfully."
        except IntegrityError:
            db.session.rollback()
            return f"Duplicate entry: {symbol} already exists."
        except Exception as e:
            db.session.rollback()
            return f"Error adding gene resource: {str(e)}"

# Function to retrieve all gene resources
def get_all_resources():
    with app.app_context():
        resources = GeneResource.query.all()
        return [r.read() for r in resources]

# Initialize the gene_resources table
def init_gene_resources():
    with app.app_context():
        db.create_all()
        logger.info("gene_resources table created.")
