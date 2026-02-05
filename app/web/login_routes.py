from .config import web_bp
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask import render_template, request, redirect, url_for, flash
from ..database.models import User


@web_bp.route('/login')
def login():
    return render_template('login.html')

@web_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('web.login')) 
    
    login_user(user)
    return redirect(url_for('web.tasks'))