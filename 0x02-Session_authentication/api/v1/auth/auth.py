#!/usr/bin/env python3
""" authentication handling module"""
from os import getenv
from typing import TypeVar, List

from flask import request


class Auth:
    """class to handle authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a path requires authentication"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """checks for authorization in the header"""
        if request is None:
            return None
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """gets the current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is not None:
            session_name = getenv('SESSION_NAME')
            return request.cookies.get(session_name)
