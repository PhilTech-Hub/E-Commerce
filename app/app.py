from flask import redirect, url_for, render_template, flash, request
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.forms import LoginForm 
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db  # Import `db` from `__init__.py`

# Import your User model
from app.models import User
from app import create_app

app = create_app()

migrate = Migrate(app, db)
login_manager = LoginManager(app)




@app.route('/create_user/<username>/<password>')
def create_user(username, password):
    # Create a new User instance
    new_user = User(username=username, password=password)
    db.session.add(new_user)  # Add the user to the session
    db.session.commit()  # Commit the session to the database
    return f"User {username} created!"




# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('home.html', name=current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Create a new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')  # Render your registration form here

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implement login logic here (check username and password)
    form = LoginForm()  # Define your LoginForm class elsewhere
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)
    

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Welcome to your dashboard, {current_user.username}!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return f'Hello, {current_user.username}!'
    else:
        return 'You are not logged in.', 401


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


