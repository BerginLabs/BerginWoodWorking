#!/usr/bin/env python3

import os
import shopify


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
    
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

    SHOPIFY_CLIENT_ID = os.environ['SHOPIFY_CLIENT_ID']
    SHOPIFY_CLIENT_SECRET = os.environ['SHOPIFY_CLIENT_SECRET']
    SHOPIFY_ACCESS_TOKEN=os.environ['SHOPIFY_ACCESS_TOKEN']
    SHOPIFY_API_VERSION="2024-01"
    SHOPIFY_STORE_NAME = '27000d-f5.myshopify.com'
    SHOPIFY_URL = f"https://{SHOPIFY_CLIENT_ID}:{SHOPIFY_CLIENT_SECRET}@{SHOPIFY_STORE_NAME}/admin"
    
    DEBUG      = True 


config = Config()

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from webapp.views.views import *
