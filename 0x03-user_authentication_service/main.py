#!/usr/bin/env python3
"""
test file
"""
import requests


BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the provided email and password.

    Args:
        email (str): User's email.
        password (str): User's password.

    Returns:
        None

    Raises:
        AssertionError: If the status code is not 200.
    """
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the provided email and incorrect password.

    Args:
        email (str): User's email.
        password (str): Incorrect password.

    Returns:
        None

    Raises:
        AssertionError: If the status code is not 401.
    """
    response = requests.post(
        f"{BASE_URL}/login", data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in with the provided email and password, returning the session ID.

    Args:
        email (str): User's email.
        password (str): User's password.

    Returns:
        str: Session ID.

    Raises:
        AssertionError: If the status code is not 200.
    """
    response = requests.post(
        f"{BASE_URL}/login", data={"email": email, "password": password})
    assert response.status_code == 200
    return response.json().get("session_id")


def profile_unlogged() -> None:
    """
    Access the user profile without logging in.

    Returns:
        None

    Raises:
        AssertionError: If the status code is not 401.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401


def profile_logged(session_id: str) -> None:
    """
    Access the user profile with a valid session ID.

    Args:
        session_id (str): Valid session ID.

    Returns:
        None

    Raises:
        AssertionError: If the status code is not 200.
    """
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Log out with a valid session ID.

    Args:
        session_id (str): Valid session ID.

    Returns:
        None

    Raises:
        AssertionError: If the status code is not 200.
    """
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Request a password reset token for the given email.

    Args:
        email (str): User's email.

    Returns:
        str: Reset token.

    Raises:
        AssertionError: If the status code is not 200.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password using a reset token.

    Args:
        email (str): User's email.
        reset_token (str): Reset token.
        new_password (str): New password.

    Returns:
        None

    Raises:
        AssertionError: If the status code is not 200.
    """
    data = {
        "email": email, "reset_token": reset_token,
        "new_password": new_password}
    response = requests.put(f"{BASE_URL}/update_password", data=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
