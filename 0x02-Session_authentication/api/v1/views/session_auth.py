#!/usr/bin/env python3
""" Module auth view
"""
from flask import Flask, request, jsonify, make_response, abort
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """verify the user login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            # Create a Session ID for the User ID
            session_id = auth.create_session(user.id)

            # Return the dictionary representation of the User
            user_dict = user.to_json()

            # Set the cookie to the response
            session_cookie_name = os.getenv('SESSION_NAME')
            response = make_response(jsonify(user_dict))
            response.set_cookie(session_cookie_name, session_id)

            return response

    # If no user with matching credentials is found
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """session logout
    """
    # Use auth.destroy_session(request) to delete the session
    if not auth.destroy_session(request):
        abort(404)

    # Return an empty JSON dictionary with status code 200
    return jsonify({}), 200
