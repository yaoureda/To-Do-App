
from .config import web_bp
from flask import render_template

@web_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')