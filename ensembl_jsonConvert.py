import requests
import json
import time

# List of gene symbols you want to fetch from Ensembl
GENES = [
    "TP53", "BRCA1", "BRCA2", "EGFR", "MYC", "APOE", "CFTR", "PTEN",
    "KRAS", "TNF", "MTHFR", "FTO", "ESR1", "AKT1", "BRAF", "CDKN2A"
]

output = []

def fetch_sequence(gene_symbol):
    for organism in ["homo_sapiens", "mus_musculus"]:
        try:
            lookup_url = f"https://rest.ensembl.org/xrefs/symbol/{organism}/{gene_symbol}?content-type=application/json"
            response = requests.get(lookup_url, timeout=10)
            if response.status_code != 200 or not response.json():
                continue

            gene_id = response.json()[0]['id']
            seq_url = f"https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/plain"
            seq_response = requests.get(seq_url, timeout=10)

            if seq_response.status_code == 200:
                return seq_response.text.strip()
        except Exception as e:
            print(f"Error fetching {gene_symbol}: {e}")
    return None

for gene in GENES:
    print(f"🔍 Fetching {gene}...")
    sequence = fetch_sequence(gene)
    if sequence:
        output.append({
            "gene": gene,
            "sequence": sequence
        })
        print(f" {gene} saved.")
    else:
        print(f" {gene} failed.")
    time.sleep(1.2)  # avoid API rate limits

# Save as JSON
with open("ensembl_sequences.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n Done. {len(output)} genes saved to ensembl_sequences.json")
