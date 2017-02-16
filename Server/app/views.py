from flask import render_template,session,redirect, flash
from app import app


##The route used to pass a user accID to the view page
@app.route('/')
def home():
    return render_template ('index.html', title="FDM TEST")
