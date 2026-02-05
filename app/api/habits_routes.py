from flask import Response, jsonify, request
from ..database.models import Habit, User
from ..database.database import db
from .config import api_bp
from flask_login import current_user, login_required

@api_bp.route('/habits', methods=['GET'])
@login_required
def get_habits():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return jsonify([habit.to_dict() for habit in habits]), 200

@api_bp.route('/habits', methods=['POST'])
@login_required
def create_habit():
    data = request.get_json()
    name = data.get("name")

    new_habit = Habit(name=name, user_id=current_user.id)
    db.session.add(new_habit)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    return jsonify(new_habit.to_dict()), 201

@api_bp.route('/habits/<int:id>', methods=['DELETE'])
@login_required
def delete_habit(id):
    habit = Habit.query.filter_by(id=id).first()
    if not habit:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(habit)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    return Response(status=204)

@api_bp.route('/streaks/<int:id>', methods=['PUT'])
@login_required
def update_streaks(id):
    data = request.get_json()
    streaks = data.get('streaks')
    
    habit = Habit.query.filter_by(id=id).first()
    habit.streaks=streaks
    db.session.add(habit)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    return Response(status=200)