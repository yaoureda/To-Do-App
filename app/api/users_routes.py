from flask import jsonify, request
from werkzeug.security import generate_password_hash
from ..database.models import User
from ..database.database import db
from .config import api_bp

@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "Conflict: username already exists"}), 409
    
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    data = {"username": new_user.username}

    return jsonify(data), 201
