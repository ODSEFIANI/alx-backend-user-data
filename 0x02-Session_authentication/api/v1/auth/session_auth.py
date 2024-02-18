#!/usr/bin/env python3
"""
Session clss module
"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session authenticationclass
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session
        """""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        # Placeholder: You might want to return the generated session_id
        return self.user_id_by_session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """fet the user id from the dictionary of given session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Based on the session id we can define the userId,
        hence return the specified instance
        """
        se_cookie = self.session_cookie(request)
        user_Id = self.user_id_for_session_id(se_cookie)
        cur_user = User.get(user_Id)
        return cur_user

    def destroy_session(self, request=None) -> bool:
        """destrit the session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return False

        # Delete the session ID
        del self.user_id_by_session_id[session_id]
        return True
