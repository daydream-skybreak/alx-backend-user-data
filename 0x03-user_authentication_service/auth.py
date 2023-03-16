#!/usr/bin/env python3
"""auth"""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """returns a salted hash of the input password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generates uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register the user to the database"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """validates if the password is valid to the users password"""
        try:
            user = self._db.find_user_by(email=email)
            valid = bcrypt.checkpw(password.encode('utf-8'),
                                   user.hashed_password)
            return valid
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a new session for the user with the email provided"""
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            self._db.update_user(user.id, session_id=id)
            return id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session: str) -> (User, None):
        """finds a user based on the session_id"""
        user = None
        if session is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int):
        """sets a user's session_id to None"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None
