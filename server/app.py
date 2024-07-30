from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(_name_)

    # Configure your database URI here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poverty.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    return app

app = create_app()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        profile_picture=data.get('profile_picture')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!', 'user_id': new_user.id}), 201
