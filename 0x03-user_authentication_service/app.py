#!/usr/bin/env python3
"""Basic Flask App"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """homepage"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    """
    registers a user to the database
    returns status code 400 if the user already exists
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
