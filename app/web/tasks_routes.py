from flask_login import current_user
from .config import web_bp
from flask import render_template

@web_bp.route('/tasks')
def tasks():
    return render_template('tasks.html', user=current_user)