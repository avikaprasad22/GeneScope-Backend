from flask import Blueprint, jsonify

gene_resource_api = Blueprint('gene_resource_api', __name__, url_prefix='/api/gene_resource')


@gene_resource_api.route("/", methods=["GET"])
def get_gene_flashcards():
    flashcards = [
        {
            "term": "Gene",
            "definition": "A segment of DNA that contains the instructions to make a protein or perform a function.",
            "example": "The BRCA1 gene helps repair DNA damage."
        },
        {
            "term": "Allele",
            "definition": "A different form of the same gene, typically one inherited from each parent.",
            "example": "You might inherit a blue-eye allele from one parent and a brown-eye allele from the other."
        },
        {
            "term": "Genotype",
            "definition": "The genetic makeup of an individual, including both dominant and recessive alleles.",
            "example": "AA, Aa, and aa are genotypes for a trait controlled by one gene."
        },
        {
            "term": "Phenotype",
            "definition": "The physical expression or traits resulting from a genotype.",
            "example": "Having blue eyes is a phenotype."
        },
        {
            "term": "Chromosome",
            "definition": "A thread-like structure made of DNA that carries genes.",
            "example": "Humans have 23 pairs of chromosomes."
        },
        {
            "term": "Mutation",
            "definition": "A change in a DNA sequence that can affect how a gene works.",
            "example": "A mutation in the TP53 gene can lead to cancer."
        },
        {
            "term": "Dominant Allele",
            "definition": "An allele that masks the effect of a recessive allele.",
            "example": "If A is dominant and a is recessive, both AA and Aa show the dominant trait."
        },
        {
            "term": "Recessive Allele",
            "definition": "An allele that is only expressed when two copies are present (homozygous).",
            "example": "The allele for cystic fibrosis is recessive."
        },
        {
            "term": "Homozygous",
            "definition": "Having two identical alleles for a gene.",
            "example": "AA or aa"
        },
        {
            "term": "Heterozygous",
            "definition": "Having two different alleles for a gene.",
            "example": "Aa"
        },
        {
            "term": "DNA",
            "definition": "Deoxyribonucleic acid; the molecule that contains the genetic instructions for life.",
            "example": "DNA is shaped like a double helix and found in the cell nucleus."
        },
        {
            "term": "RNA",
            "definition": "A molecule that helps decode DNA into proteins.",
            "example": "Messenger RNA (mRNA) carries instructions from DNA to ribosomes."
        },
        {
            "term": "Protein",
            "definition": "A molecule made from amino acids that performs various functions in the body.",
            "example": "Hemoglobin is a protein that carries oxygen in blood."
        },
        {
            "term": "Codon",
            "definition": "A three-nucleotide sequence in mRNA that codes for an amino acid.",
            "example": "AUG is the start codon that signals the beginning of protein synthesis."
        },
        {
            "term": "Genome",
            "definition": "The complete set of DNA, including all of an organism’s genes.",
            "example": "The Human Genome Project mapped all the genes in human DNA."
        }
    ]
    return jsonify(flashcards)
