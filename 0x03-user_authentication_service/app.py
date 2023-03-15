#!/usr/bin/env python3
"""Basic Flask App"""

from flask import Flask, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', method=['GET'])
def home():
    """homepage"""
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
