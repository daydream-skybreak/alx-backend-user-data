#!/usr/bin/env python3
"""basic authentication module"""
import re

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """handles basic authorization"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extracts base64 authorization header"""
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None
        if len(authorization_header.split()) < 2:
            return None
        if authorization_header.split()[0] == "Basic":
            return authorization_header.split()[1]
