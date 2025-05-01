from flask import Blueprint, jsonify
import requests, random, string
from model.gene_resource import GeneResource, add_gene_resource, get_all_resources
from __init__ import db, app
from sqlalchemy.exc import IntegrityError

gene_resources_api = Blueprint('gene_resources_api', __name__, url_prefix="/api")

GENE_API_URL = "https://clinicaltables.nlm.nih.gov/api/ncbi_genes/v3/search"

def fetch_gene_records():
    try:
        random_term = random.choice(string.ascii_uppercase)
        params = {
            "terms": random_term,
            "count": 200,
            "df": "chromosome,Symbol,description,type_of_gene,GeneID",
        }
        resp = requests.get(GENE_API_URL, params=params)
        resp.raise_for_status()
        return resp.json()[3]
    except Exception as e:
        print(f"[fetch_gene_records] error: {e}")
        return []

@gene_resources_api.route('/gene_resources', methods=['GET'])
def get_gene_resources():
    gene_data = fetch_gene_records()
    gene_data = [g for g in gene_data if all(g)]

    new_resources = []
    for chrom, symbol, desc, gene_type, gene_id in gene_data:
        existing = db.session.query(GeneResource).filter_by(symbol=symbol).first()
        if not existing:
            resource = GeneResource(
                symbol=symbol,
                description=desc,
                chromosome=chrom,
                gene_type=gene_type,
                gene_id=gene_id
            )
            db.session.add(resource)
            new_resources.append(resource)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Duplicate entry or DB error"}), 500

    def format_friendly(r):
        gene_type_explanation = {
            "protein-coding": "This gene provides instructions for making a protein, which plays a specific role in your body.",
            "pseudogene": "This is a pseudogene, meaning it resembles a gene but is typically nonfunctional.",
            "ncRNA": "This gene does not code for a protein but produces non-coding RNA, which can regulate gene expression.",
            "tRNA": "This gene makes transfer RNA (tRNA), which helps assemble proteins from amino acids.",
            "rRNA": "This gene produces ribosomal RNA (rRNA), a key part of ribosomes, the protein factories of cells.",
            "snRNA": "This gene produces small nuclear RNA involved in RNA processing.",
            "miscRNA": "This gene produces other types of RNA with various cellular functions."
        }

        chromosome_descriptions = {
            "1": "Chromosome 1 is the largest and contains many genes linked to brain development and cancer.",
            "2": "Chromosome 2 includes genes involved in sensory perception and neurological function.",
            "3": "Chromosome 3 is linked to vision, hearing, and immune system regulation.",
            "4": "Chromosome 4 includes genes related to skeletal development and Huntington’s disease.",
            "5": "Chromosome 5 plays roles in growth and development, including limb formation.",
            "6": "Chromosome 6 holds genes important for the immune system, including HLA genes.",
            "7": "Chromosome 7 is associated with cystic fibrosis and other genetic disorders.",
            "8": "Chromosome 8 has genes important for brain development and cancer susceptibility.",
            "9": "Chromosome 9 includes genes for blood type and skin development.",
            "10": "Chromosome 10 carries genes linked to hearing and metabolic disorders.",
            "11": "Chromosome 11 has genes involved in insulin production and sickle cell disease.",
            "12": "Chromosome 12 includes genes for hormone signaling and muscle development.",
            "13": "Chromosome 13 is related to eye development and some rare cancers.",
            "14": "Chromosome 14 has genes important for the immune response and early development.",
            "15": "Chromosome 15 is linked to conditions like Angelman and Prader-Willi syndromes.",
            "16": "Chromosome 16 contains genes involved in kidney function and metabolism.",
            "17": "Chromosome 17 includes BRCA1, a gene related to breast and ovarian cancer risk.",
            "18": "Chromosome 18 is connected to developmental disorders and cell organization.",
            "19": "Chromosome 19 is gene-rich and plays a role in lipid metabolism.",
            "20": "Chromosome 20 includes genes associated with diabetes and immune regulation.",
            "21": "Chromosome 21 is best known for its link to Down syndrome.",
            "22": "Chromosome 22 contains genes important for hearing and neural connectivity.",
            "X": "The X chromosome carries many genes vital for development and is involved in sex-linked disorders.",
            "Y": "The Y chromosome determines male sex characteristics and contains few active genes.",
            "MT": "Mitochondrial DNA (MT) is inherited from the mother and powers cell energy production."
        }

        gene_type_desc = gene_type_explanation.get(r.gene_type.lower(), "This gene has a specialized role in cellular function.")
        chrom_info = chromosome_descriptions.get(r.chromosome, "Chromosome information not clearly defined.")

        return {
            "symbol": r.symbol,
            "friendly_name": f"{r.symbol} — {r.description.split(',')[0] if ',' in r.description else r.description}",
            "description": r.description,
            "chromosome": r.chromosome,
            "chromosome_info": chrom_info,
            "gene_type": r.gene_type,
            "gene_type_info": gene_type_desc,
            "gene_id": r.gene_id,
            "learn_more_link": f"https://www.ncbi.nlm.nih.gov/gene/{r.gene_id}"
        }

    all_resources = db.session.query(GeneResource).all()
    return jsonify([format_friendly(r) for r in all_resources])
