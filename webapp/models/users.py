#!/usr/bin/env python3

import uuid

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db, login_manager


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    user_email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    
    email_verified = db.Column(db.Boolean, nullable=False)
    phone_verified = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    
    user_image = db.Column(db.Text, nullable=True)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"<User {self.user_id}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
