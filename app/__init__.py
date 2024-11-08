# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from .models import User  # Ensure this imports your User model
from .db import db

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/lenovo/Desktop/Projects/Python Projects/E-Market/instance/ecommerce.db'  # Replace with your database URI
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['PAYPAL_CLIENT_ID'] = 'your_client_id'
    app.config['PAYPAL_CLIENT_SECRET'] = 'your_client_secret'
    app.config['PAYPAL_MODE'] = 'sandbox'  # Use 'live' for production
    app.config['DEBUG'] = True  # Add this line

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    
    
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register the Blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
