from flask_login import current_user
from .config import web_bp
from flask import render_template

@web_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=current_user)