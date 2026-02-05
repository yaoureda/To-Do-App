from .config import web_bp
import requests
from flask import render_template, request, redirect, url_for, flash

@web_bp.route('/signup')
def signup():
    return render_template('signup.html')
