#!/usr/bin/env python3
"""Basic Flask App"""
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """implements a login method"""
    email, pswd = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email, pswd):
        session = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie(session)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """implements logout method"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return 403
    AUTH.destroy_session(user.id)
    return redirect('/')

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
    except NoResultFound:
        return 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
