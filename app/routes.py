from app import app
from flask import render_template, send_from_directory

# Basic route
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
