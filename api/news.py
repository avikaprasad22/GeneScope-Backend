from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = "68a69dddbb9341d0a5f8fe2aa38967fd"

@app.route('/api/science-news')
def get_science_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'category': 'science',
        'language': 'en',
        'pageSize': 10,
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)