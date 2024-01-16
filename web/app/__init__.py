from flask import Flask 

app = Flask(__name__)
app.secret_key = '65ae6eb20bc04202aacf7d57dec0febb'

from app import routes
