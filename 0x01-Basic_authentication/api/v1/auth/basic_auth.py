#!/usr/bin/env python3
"""basic authentication module"""
import base64
import binascii
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns decoded value of base64 string"""
        if type(base64_authorization_header) == str:
            try:
                response = base64.b64decode(base64_authorization_header,
                                            validate=True)
                return response.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """returns user email and password from base64 decoded value"""
        if type(decoded_base64_authorization_header) == str and\
                ':' in decoded_base64_authorization_header:
            return tuple(decoded_base64_authorization_header.split(':'))
        else:
            return (None, None)
