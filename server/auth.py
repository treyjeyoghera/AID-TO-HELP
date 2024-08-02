from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid email or password'}, 401
        
        login_user(user)
        return {'message': 'Logged in successfully'}

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return {'message': 'Email address already exists'}, 400

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}

class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return {'message': 'Logged out successfully'}

def initialize_auth_routes(api):
    api.add_resource(LoginResource, '/login')
    api.add_resource(SignupResource, '/signup')
    api.add_resource(LogoutResource, '/logout')
