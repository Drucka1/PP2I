from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy 
import secrets, os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance', 'userbase.db'))
db = SQLAlchemy(app) 

secretKey = secrets.token_hex(32)
app.config['SECRET_KEY'] = secretKey
bcrypt = Bcrypt(app)                                # Password hashing

class User(db.Model, UserMixin):                               # User database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

with app.app_context():
    db.create_all()
    
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# Home page

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)

    return render_template('index.html')


# Login screen 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'), email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('index'))
 
@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()


# Error page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Profile page

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user= current_user)

if __name__ == "__main__":
    app.run(debug=True)
