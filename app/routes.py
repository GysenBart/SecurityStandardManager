from app import app
from flask import render_template, send_from_directory, flash, redirect, url_for, request
from app.util import check_and_clone, update_manager
from app.database_handler import proces_excel_data
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
@app.route('/update_standards', methods=['POST'])
def update_standards():
    # Logic to execute when the button is pressed
    check_and_clone()
    print("Function executed!")
    flash("Custom function executed successfully!", "success")
    return redirect(url_for('admin.index'))  # Redirect back to the admin index

@app.route('/handle_update', methods=['POST'])
def handle_update():
    update_manager.disable_update()
    start_column = request.form['comment']
    print("Update comment:", start_column)
    
    # When the start column for the standards is set, we can process the excel data
    #proces_excel_data(start_column)
    
    # Process the input as needed...
    flash("Update info submitted!", "success")
    return redirect(url_for('admin.index'))
