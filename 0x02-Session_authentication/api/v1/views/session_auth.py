#!/usr/bin/env python3
"""handles all routes for the Session authentication"""
from os import getenv

from flask import Flask, request, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models.user import User

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.route('/auth_session/login', method='POST', strict_slashes=False)
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if email is None or len(email.strip()) == 0:
        return jsonify({'error': 'email missing'}), 400

    if password is None or len(password.strip()) == 0:
        return jsonify({'error':"password missing"}), 401
    try:
        users = User.search({'email': email})
    except Exception:
           return jsonify({'email':"no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], id))
        response = jsonify(users[0].to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)
        return response
    return jsonify({'error': 'wrong password'}), 401

