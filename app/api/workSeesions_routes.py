from flask import Response, jsonify, request
from ..database.models import WorkSession
from ..database.database import db
from .config import api_bp
from flask_login import current_user, login_required

@api_bp.route('/session', methods=['GET'])
@login_required
def get_sessions():
    sessions = WorkSession.query.filter_by(user_id=current_user.id).all()
    stats = {s.date: s.minutes for s in sessions}
    return jsonify(stats), 200

@api_bp.route('/session', methods=['POST'])
@login_required
def create_session():
    data = request.get_json()
    date = data.get("date")
    minutes = data.get("minutes")

    existing = WorkSession.query.filter_by(date=date).first()
    if not existing:
        new_session = WorkSession(date=date, minutes=minutes, user_id=current_user.id)
        db.session.add(new_session)
    else:
        existing.minutes += minutes
        db.session.add(existing)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    return jsonify({"success": True}), 201

@api_bp.route("/session", methods=["DELETE"])
@login_required
def delete_work_sessions():
    WorkSession.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"success": True})
