from flask import Response, jsonify, request
from ..database.models import Task
from ..database.database import db
from .config import api_bp
from flask_login import current_user, login_required

@api_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@api_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    name = data.get("name")
    deadline = data.get("deadline")

    new_task = Task(name=name, deadline=deadline, user_id=current_user.id)
    db.session.add(new_task)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    return jsonify(new_task.to_dict()), 201

@api_bp.route('/tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(task)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    return Response(status=204)