from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import secrets
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
bcrypt = Bcrypt(app)  # Password hashing

class User(UserMixin):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

def init_db():
    conn = sqlite3.connect('instance/userbase.db')
    cursor = conn.cursor()

    with app.open_resource('instance/schema.sql', mode='r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect('instance/userbase.db')
        g.db.row_factory = sqlite3.Row
    return g.db

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(*user_data)
    return None

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
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        conn = get_db_connection()
        user_data = conn.execute(
            'SELECT * FROM user WHERE username = ? OR email = ?', (username_or_email, username_or_email)
        ).fetchone()
        conn.close()

        if user_data and User(*user_data).check_password(password):
            user = User(*user_data)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('register.html')

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            conn.execute('INSERT INTO user (username, password, email) VALUES (?, ?, ?)', (username, hashed_password, email))
            conn.commit()
            conn.close()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Profile page
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
