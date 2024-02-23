#!/usr/bin/env python3
"""
py module: AUTHENTICATION
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
import uuid
from typing import Union
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ encrypt a password according to the
    hash mechanisme"""
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """generates UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth clss
    """

    def __init__(self):
        """init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Create a user and use method from DB"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ REturns boolean that verify if the user exists"""
        try:
            va_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if checkpw(password.encode("utf-8"), va_user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """generates user ID """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_id=user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """return the coresponding user object from
        a given session id"""
        if type(session_id) != str:
            return None
        try:
            se_user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return se_user

    def destroy_session(self, user_id: int) -> None:
        """destroy a session of given user
        seting it to NONE"""
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """generates resest_token for a given user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """check the reset token and update the hashed_password
        accordignly"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, hashed_password=_hash_password(password))
        self._db.update_user(user.id, reset_token=None)
        return None
