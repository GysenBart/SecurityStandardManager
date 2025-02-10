from app import app
from flask import render_template, send_from_directory, flash, redirect, url_for

# Basic route
#@app.route('/')
#def index():
    #return render_template('index.html')
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/')
def home():
    return redirect(url_for('admin.index'))

# Flask route for the button action
@app.route('/execute_function', methods=['POST'])
def execute_function():
    # Logic to execute when the button is pressed
    print("Function executed!")
    flash("Custom function executed successfully!", "success")
    return redirect(url_for('admin.index'))  # Redirect back to the admin index