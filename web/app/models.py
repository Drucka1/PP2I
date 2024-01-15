from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    gender = db.Column(db.String(20))
    budget = db.Column(db.Float)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    servings_unit = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class RecipeCategory(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    line = db.Column(db.Integer, primary_key=True)
    amount_int = db.Column(db.Integer, nullable=False)
    amount_num = db.Column(db.Integer, nullable=False)
    amount_denom = db.Column(db.Integer, nullable=False)
    amount_float = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(2), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

class Instruction(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    line = db.Column(db.Integer, primary_key=True)
    txt = db.Column(db.Text, nullable=False)

class IngredientSection(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    line = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)

class InstructionSection(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    line = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
