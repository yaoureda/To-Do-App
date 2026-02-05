from .config import web_bp
import requests
from flask import render_template, request, redirect, url_for, flash

@web_bp.route('/signup')
def signup():
    return render_template('signup.html')

@web_bp.route('/signup', methods=['POST'])
def signup_post():
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

    # Compute full API URL
    api_url = request.url_root.rstrip("/") + url_for("api.create_user")

    try:
        response = requests.post(api_url, json={"username": username, "password": password})
    except requests.exceptions.RequestException:
        flash("Server error. Please try again later.")
        return redirect(url_for("web.signup"))

    if response.status_code == 409:
        flash("Username already exists")
        return redirect(url_for("web.signup"))

    if response.status_code != 201:
        flash("Invalid or missing username or password.")
        return redirect(url_for("web.signup"))

    return redirect(url_for("web.login"))
