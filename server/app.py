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

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': user.profile_picture
        }), 200
    return jsonify({'message': 'User not found!'}), 404 

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']

    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'}), 200
    return jsonify({'message': 'User not found!'}), 404

if _name_ == '_main_':
    app.run(debug=True)
