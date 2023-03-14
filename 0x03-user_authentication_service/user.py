#!/usr/bin/env python3
"""
User Model created by SQLAlchemy
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String

Base = declarative_base()


class User(Base):
    """user model of a sql database table named user"""
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
