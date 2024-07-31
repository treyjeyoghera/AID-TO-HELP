from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from models import db, User, Employment, Category, Application, SocialIntegration

def create_app():
    app = Flask(__name__)

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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': user.profile_picture
        } for user in users
    ]), 200

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

@app.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category:
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description,
        }), 200
    return jsonify({'message': 'Category not found'}), 404

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
        } for category in categories
    ]), 200

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or not all(key in data for key in ['name']):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_category = Category(
        name=data['name'],
        description=data.get('description'),
        user_id=data.get('user_id')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully!', 'category_id': new_category.id}), 201

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'message': 'Category not found!'}), 404

    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Category updated successfully!'}), 200

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully!'}), 200
    return jsonify({'message': 'Category not found!'}), 404

@app.route('/employments', methods=['POST'])
def create_employment():
    data = request.get_json()
    if not data or not all(key in data for key in ['user_id', 'category_id', 'title', 'description']):
        return jsonify({'message': 'Missing required fields!'}), 400

    employment = Employment.create(
        user_id=data['user_id'],
        category_id=data['category_id'],
        title=data['title'],
        description=data['description'],
        requirements=data.get('requirements'),
        location=data.get('location'),
        salary_range=data.get('salary_range')
    )
    return jsonify({'message': 'Employment created successfully!', 'employment_id': employment.id}), 201

@app.route('/employments', methods=['GET'])
def get_employments():
    employments = Employment.get_all()
    return jsonify([
        {
            'id': employment.id,
            'user_id': employment.user_id,
            'category_id': employment.category_id,
            'title': employment.title,
            'description': employment.description,
            'requirements': employment.requirements,
            'location': employment.location,
            'salary_range': employment.salary_range
        } for employment in employments
    ]), 200

@app.route('/employments/<int:id>', methods=['GET'])
def get_employment(id):
    employment = Employment.get_by_id(id)
    if employment:
        return jsonify({
            'id': employment.id,
            'user_id': employment.user_id,
            'category_id': employment.category_id,
            'title': employment.title,
            'description': employment.description,
            'requirements': employment.requirements,
            'location': employment.location,
            'salary_range': employment.salary_range
        }), 200
    return jsonify({'message': 'Employment not found!'}), 404

@app.route('/employments/<int:id>', methods=['PUT'])
def update_employment(id):
    employment = Employment.get_by_id(id)
    if not employment:
        return jsonify({'message': 'Employment not found!'}), 404

    data = request.get_json()
    employment.update(
        title=data.get('title'),
        description=data.get('description'),
        requirements=data.get('requirements'),
        location=data.get('location'),
        salary_range=data.get('salary_range')
    )
    return jsonify({'message': 'Employment updated successfully!'}), 200

@app.route('/employments/<int:id>', methods=['DELETE'])
def delete_employment(id):
    employment = Employment.get_by_id(id)
    if employment:
        employment.delete()
        return jsonify({'message': 'Employment deleted successfully!'}), 200
    return jsonify({'message': 'Employment not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
