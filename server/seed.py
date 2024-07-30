from faker import Faker
from models import db, User, Employment, Category, Application, SocialIntegration
from app import create_app  # assuming your Flask app factory function is named create_app
import random

# Initialize Faker
fake = Faker()

# Create Flask app and context
app = create_app()
app.app_context().push()

# Create all tables
db.create_all()

# Seed Users
def seed_users(n=100):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            profile_picture=fake.image_url()
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    return users

# Seed Categories
def seed_categories(users, n=100):
    categories = []
    for _ in range(n):
        category = Category(
            name=fake.word(),
            description=fake.text(),
            user_id=random.choice(users).id
        )
        categories.append(category)
    db.session.add_all(categories)
    db.session.commit()
    return categories

# Seed Employments
def seed_employments(users, categories, n=100):
    employments = []
    for _ in range(n):
        employment = Employment(
            user_id=random.choice(users).id,
            category_id=random.choice(categories).id,
            title=fake.job(),
            description=fake.text(),
            requirements=fake.text(),
            location=fake.city(),
            salary_range=random.randint(30000, 120000)
        )
        employments.append(employment)
    db.session.add_all(employments)
    db.session.commit()
    return employments

# Seed Applications
def seed_applications(users, employments, n=100):
    applications = []
    for _ in range(n):
        application = Application(
            user_id=random.choice(users).id,
            employment_id=random.choice(employments).id,
            status=random.randint(0, 3)  # Assuming you have 4 statuses
        )
        applications.append(application)
    db.session.add_all(applications)
    db.session.commit()
    return applications

# Seed Social Integrations
def seed_social_integrations(users, categories, n=100):
    social_integrations = []
    for _ in range(n):
        social_integration = SocialIntegration(
            user_id=random.choice(users).id,
            category_id=random.choice(categories).id
        )
        social_integrations.append(social_integration)
    db.session.add_all(social_integrations)
    db.session.commit()
    return social_integrations

# Seed all data
def seed_all():
    users = seed_users()
    categories = seed_categories(users)
    employments = seed_employments(users, categories)
    applications = seed_applications(users, employments)
    social_integrations = seed_social_integrations(users, categories)

if __name__ == '__main__':
    seed_all()
