#!/usr/bin/env python3
"""Expiration data for session id"""
import datetime
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """class implementation of expiration data for session ids"""
    def __init__(self):
        """initialization method"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """creates a session id"""
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """gets user_id based on session_id"""
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            time_diff = datetime.timedelta(seconds=self.session_duration)
            current_time = datetime.datetime.now()
            if session_dict['created_at'] + time_diff < current_time:
                return None
            return session_dict['user_id']
