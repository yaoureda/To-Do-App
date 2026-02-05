from .config import web_bp
from flask import render_template

@web_bp.route('/habits')
def habits():
    return render_template('habits.html')