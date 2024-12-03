from app import app
from flask import render_template

# Basic route
@app.route('/')
def index():
    return "Hello bitch"
    #return render_template('index.html')