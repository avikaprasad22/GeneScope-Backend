import csv
import json
import random

input_file = "variant_summary.txt"  # Make sure this file is in the same folder
output_file = "mutation_dataset.json"

# Define valid mutation types
VALID_TYPES = {
    "single nucleotide variant": "substitution",
    "deletion": "deletion",
    "insertion": "insertion"
}

filtered_data = []

with open(input_file, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        gene = row["GeneSymbol"]
        condition = row["PhenotypeList"]
        mutation_type = row["Type"]

        if mutation_type in VALID_TYPES and condition:
            filtered_data.append({
                "gene": gene,
                "mutation": VALID_TYPES[mutation_type],
                "condition": condition.split(",")[0].strip()
            })

# Randomize and limit
random.shuffle(filtered_data)
filtered_data = filtered_data[:1000]

# Save to JSON
with open(output_file, "w") as out:
    json.dump(filtered_data, out, indent=2)

print(f"✅ Saved {len(filtered_data)} mutations to {output_file}")