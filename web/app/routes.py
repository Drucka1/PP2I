from flask import render_template, g, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from app import app, db
from app.models import User, Recipe
from app.aux import deleteOccurences, deleteOccurencesIngredients, search
import sqlite3
import os

bcrypt = Bcrypt(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db_path = os.path.join(app.root_path, '../instance', 'site.db')
        db = g._database = sqlite3.connect(db_path)
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def home():
    user = User.query.get(session.get('user_id')) if 'user_id' in session else None

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT title, imageURL, id FROM recipes')
    recipes_data = deleteOccurences(cursor.fetchall())

    if request.method == 'GET':
        query = request.args.get('query', '')
        recipes_data = search(query, recipes_data)

    return render_template('home.html', user=user, recipes=recipes_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            flash("Passwords do not match")
            return render_template('register.html')

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
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('profile.html', user=user)
    flash('You need to log in to access this page.', 'warning')
    return redirect(url_for('login'))

@app.route('/recipes/<int:recipeId>')
def recipe(recipeId):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.title,
                r.imageURL,
                c.name as category,
                ig.name as ingredient_name,
                i.amountint,
                i.amountnum,
                i.amountdenom,
                i.amountfloat,
                i.unit,
                ig.price,
                ins.txt as instruction_text
            FROM recipes as r
            JOIN category as rc ON r.id = rc.recipeid
            JOIN categories as c ON rc.categoryid = c.id
            LEFT JOIN ingredient as i ON r.id = i.recipeid
            LEFT JOIN ingredients as ig ON i.ingredientid = ig.id
            LEFT JOIN instruction as ins ON r.id = ins.recipeid
            WHERE r.id = ?
        """, (recipeId,))

        rows = cursor.fetchall()
        if not rows:
            return render_template('not_found.html', message='Recipe not found')

        recipeData = {
            'title': rows[0][0],
            'imageURL': rows[0][1],
            'category': rows[0][2],
            'ingredients': [],
            'instructions' : [],
            'price': 0
        }

        for row in rows:
            if row[3]:  
                ingredient = {
                    'name': row[3],
                    'amountint': row[4],
                    'amountnum': row[5],
                    'amountdenom': row[6],
                    'amountfloat': row[7],
                    'unit': row[8],
                    'price': row[9]
                }

                recipeData['ingredients'].append(ingredient)
            
            if row[10]:
                instruction = {
                    'text': row[10]
                }
                recipeData['instructions'].append(instruction)        
        
        recipeData['ingredients'] = deleteOccurencesIngredients(recipeData['ingredients'])
        recipeData['instructions'] = deleteOccurencesIngredients(recipeData['instructions'])
        recipeData['price'] = sum([ig.get('price') for ig in recipeData['ingredients']])

        return render_template('recipe.html', recipeData=recipeData)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html')


@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            if request.method == 'POST':

                gender = request.form['gender']
                budget = request.form['budget'] 

                user.gender = gender
                user.budget = budget
                db.session.commit()
                
                return redirect(url_for('profile'))

            return render_template('preferences.html', user=user)

    flash('You need to log in to access this page.', 'warning')
    return redirect(url_for('login'))
