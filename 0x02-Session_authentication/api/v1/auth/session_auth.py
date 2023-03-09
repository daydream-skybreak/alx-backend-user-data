#!/usr/bin/env python3
"""Session auth"""
from api.v1.auth.auth import Auth
import uuid
from os import getenv

from models.user import User


class SessionAuth(Auth):
    """Session authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns user_id based on session id"""
        if type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns user instance based on a cookie value"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)
