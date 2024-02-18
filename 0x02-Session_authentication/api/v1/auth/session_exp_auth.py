#!/usr/bin/env python3
"""
how long the cookies last module
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration"""

    def __init__(self):
        super().__init__()
        # Assign session_duration from the environment variable
        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration) if session_duration else 0
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a Session ID by calling the parent class method.

        :param user_id: User ID for which the session is created.
        :return: Session ID created or None if it fails.
        """
        session_id = super().create_session(user_id)

        if session_id:
            # Create a session dictionary
            session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()
            }

            # Set the session dictionary as the value for the session_id key
            self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the User ID for a given Session ID.

        :param session_id: Session ID to look up.
        :return: User ID if session is valid, otherwise None.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        user_id = session_dict.get("user_id")

        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get("created_at")

        if created_at is None or (created_at + timedelta(seconds=self.session_duration)) < datetime.now():
            return None

        return user_id