from flask import render_template, g, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from app import app, db
from app.models import User
import sqlite3
import os

bcrypt = Bcrypt(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db_path = os.path.join(app.root_path, '../instance', 'site.db')
        print(f"Database Path: {db_path}")
        db = g._database = sqlite3.connect(db_path)
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    user = User.query.get(session.get('user_id')) if 'user_id' in session else None

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT title, imageURL FROM recipes')
    recipes_data = cursor.fetchall()

    return render_template('home.html', user=user, recipes=recipes_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    # Retrieve the user from the database based on the user_id stored in the session
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('profile.html', user=user)
    flash('You need to log in to access this page.', 'warning')
    return redirect(url_for('login'))

