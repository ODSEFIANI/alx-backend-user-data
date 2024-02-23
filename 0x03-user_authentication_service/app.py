#!/usr/bin/env python3
""" endpoint Module """
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    """default route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def generate_user():
    """generate a new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": "{}".format(email), "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """generates a user_session """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    responce = jsonify({"email": email, "message": "logged in"})
    session_id = AUTH.create_session(email)
    responce.set_cookie("session_id", session_id)
    return responce


@app.route("/sessions", methods=["DELETE"])
def logout():
    """removes a user_session"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")

@app.route("/profile")
def profile():
    """fetch the user_profile"""
    session_id = request.cookies.get("session_id")
    the_user = AUTH.get_user_from_session_id(session_id)
    if the_user is None:
        abort(403)
    return jsonify({"email": the_user.email})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")