from .config import web_bp, BASE_URL
import requests
from flask import render_template, request, redirect, url_for, flash

@web_bp.route('/signup')
def signup():
    return render_template('signup.html')

@web_bp.route('/signup', methods=['POST'])
def signup_post():

    username = request.form.get('username')
    password = request.form.get('password')

    response = requests.post(f"{BASE_URL}/api/users", json={"username": username, "password": password})

    if response.status_code == 409:
        flash('Username already exists')
        return redirect(url_for('web.signup'))
      
    if response.status_code != 201:
        flash('Invalid or missing username or password.')
        return redirect(url_for('web.signup'))

    return redirect(url_for('web.login'))