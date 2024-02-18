#!/usr/bin/env python3
""" Module auth view
"""
from flask import Flask, request, jsonify, abort, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """verify the user login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing or empty
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the User ID
    session_id = auth.create_session(user.id)

    # Return the dictionary representation of the User
    user_dict = user.to_json()

    # Set the cookie to the response
    session_cookie_name = app.config.get('SESSION_NAME')
    response = make_response(jsonify(user_dict))
    response.set_cookie(session_cookie_name, session_id)

    return response

