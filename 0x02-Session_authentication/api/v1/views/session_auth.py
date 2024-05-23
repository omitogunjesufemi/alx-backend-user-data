#!/usr/bin/env python3
"""
A Flask view that handles all routes for the Session Authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Login method
    """
    if request is None:
        return None

    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    User.load_from_file()
    usr_attr = {"email": email}
    user_list = User.search(usr_attr)
    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]
    if user.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response
