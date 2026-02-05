from .config import web_bp
from flask import render_template

@web_bp.route('/')
def index():
    return render_template('index.html')