from flask import Flask
from flask_cors import CORS
from api.illumina import illumina_api  # Your Blueprint

app = Flask(__name__)

# ✅ CORS: This allows requests from your frontend
CORS(app, origins=["http://127.0.0.1:4504"], supports_credentials=True)

@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:4504"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# ✅ Register your API routes
app.register_blueprint(illumina_api)

if __name__ == '__main__':
    app.run(debug=True, port=8504)