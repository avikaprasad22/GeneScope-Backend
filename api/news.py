from flask import Blueprint, jsonify, request
import requests
import os

news_api = Blueprint('news_api', __name__)

API_KEY = os.getenv("NEWS_API_KEY")

# Top Headlines Endpoint
@news_api.route('/api/science-news')
def get_science_news():
    params = {
        'apiKey': API_KEY,
        'category': request.args.get('category', 'science'),
        'language': request.args.get('language', 'en'),
        'pageSize': request.args.get('pageSize', 10),
        'q': request.args.get('q'),
        'from': request.args.get('from'),
        'to': request.args.get('to'),
        'sortBy': request.args.get('sortBy'),
        'domains': request.args.get('domains'),
        'excludeDomains': request.args.get('excludeDomains'),
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get("https://newsapi.org/v2/top-headlines", params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e), 'message': response.text}), 500

# Everything Endpoint
@news_api.route('/api/everything-news')
def get_everything_news():
    params = {
        'apiKey': API_KEY,
        'q': request.args.get('q'),  # required
        'language': request.args.get('language', 'en'),
        'pageSize': request.args.get('pageSize', 10),
        'from': request.args.get('from'),
        'to': request.args.get('to'),
        'sortBy': request.args.get('sortBy'),
        'domains': request.args.get('domains'),
        'excludeDomains': request.args.get('excludeDomains'),
    }

    params = {k: v for k, v in params.items() if v is not None}

    if 'q' not in params:
        return jsonify({'error': "Missing required parameter: 'q'"}), 400

    try:
        response = requests.get("https://newsapi.org/v2/everything", params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e), 'message': response.text}), 500
