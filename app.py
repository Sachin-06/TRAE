from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
import os
from dotenv import load_dotenv
from extensions import db, migrate, bootstrap, login_manager

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///foodforward.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with app
db.init_app(app)
migrate.init_app(app, db)
bootstrap.init_app(app)
login_manager.init_app(app)

# Import models and routes after initializing db to avoid circular imports
from models import User, Donation, Delivery, Recipient
from routes import register_routes

# Register all routes
register_routes(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)