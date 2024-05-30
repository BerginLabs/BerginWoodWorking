#!/usr/bin/env python3

import os

from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

class Config:
    SECRET_KEY = os.environ['BWW_SECRET_KEY']
    DB_HOST    = os.environ.get('BWW_DB_HOST') or "localhost"
    DB_PORT    = os.environ.get('BWW_DB_PORT') or 3306
    DB_USER    = os.environ.get('BWW_DB_USER') or "appuser"
    DB_PASSWD  = os.environ['BWW_DB_PASSWD']
    DB_NAME    = os.environ.get('BWW_DB_NAME') or "BerginWoodWorking"
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG      = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

config = Config()

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from webapp.views.views import *
