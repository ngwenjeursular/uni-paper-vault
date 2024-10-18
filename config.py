"""
Configuration settings
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



basedir = os.path.abspath(os.path.dirname(__file__))

print("Config file loaded.")


class Config:
    DEBUG = False
    TESTING = False
    # Base directory for your application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Upload folder path
    UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    m_key = '0a619fb395d0f3b8b2975cf7fd54593b0316f86bf2dc0517'
    SECRET_KEY = os.environ.get('SECRET_KEY') or m_key

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 1)
    


