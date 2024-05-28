#!/usr/bin/env python3

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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

config = Config()

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)