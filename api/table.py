import kagglehub

# Download latest version
path = kagglehub.dataset_download("vivmankar/physics-vs-chemistry-vs-biology")

print("Path to dataset files:", path)


from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("vivmankar/physics-vs-chemistry-vs-biology")

@app.route('/get_data', methods=['GET'])
def get_data():
    subject = request.args.get('subject', 'Biology')  # Default to Biology
    filtered_df = df[df['Subject'] == subject]  # Adjust based on dataset structure
    return jsonify(filtered_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
