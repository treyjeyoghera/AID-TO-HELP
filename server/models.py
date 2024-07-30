from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    _tablename_ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    profile_picture = db.Column(db.String)

    # Relationships
    employments = db.relationship('Employment', back_populates='user', lazy=True)
    applications = db.relationship('Application', back_populates='user', lazy=True)
    categories = db.relationship('Category', back_populates='creator', lazy=True)
    social_integrations = db.relationship('SocialIntegration', back_populates='user', lazy=True)