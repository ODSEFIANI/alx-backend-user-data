#!/usr/bin/env python3
"""
Session clss module
"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session authenticationclass
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        # Placeholder: You might want to return the generated session_id
        return self.user_id_by_session_id
