#!/usr/bin/env python3

import uuid

from webapp import db


class UpcomingEvents(db.Model):
    __tablename__ = "upcoming_events"
    
    event_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"<User {self.event_id}>"
