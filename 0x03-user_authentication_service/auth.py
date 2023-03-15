#!/usr/bin/env python3
"""auth"""
from db import DB
import bcrypt
from user import User


def _hash_password(password: str) -> bytes:
    """returns a salted hash of the input password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register the user to the database"""
        if self._db.find_user_by(email=email):
            raise ValueError(f'User {email} already exists')
        return self._db.add_user(email, _hash_password(password))