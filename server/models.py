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

    class Employment(db.Model):
        _tablename_ = 'employment'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    location = db.Column(db.String)
    salary_range = db.Column(db.Integer)

    # Relationships
    user = db.relationship('User', back_populates='employments')  # Corrected relationship
    category = db.relationship('Category', back_populates='employments', lazy=True)
    applications = db.relationship('Application', back_populates='employment', lazy=True)

class Category(db.Model):
    _tablename_ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    employments = db.relationship('Employment', back_populates='category', lazy=True)
    social_integrations = db.relationship('SocialIntegration', back_populates='category', lazy=True)
    creator = db.relationship('User', back_populates='categories', lazy=True)
    
class Application(db.Model):
    _tablename_ = 'application'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employment_id = db.Column(db.Integer, db.ForeignKey('employment.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)  # You can define constants for status

    # Relationships
    user = db.relationship('User', back_populates='applications', lazy=True)
    employment = db.relationship('Employment', back_populates='applications', lazy=True)

class SocialIntegration(db.Model):
    _tablename_ = 'socialintegration'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='social_integrations', lazy=True)
    category = db.relationship('Category', back_populates='social_integrations', lazy=True)