from .database import db
from datetime import timezone, datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    habits = db.relationship(
        "Habit",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    work_sessions = db.relationship(
        "WorkSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="tasks")

    created_at = db.Column(
        db.Text(),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'deadline': self.deadline,
            'created_at': self.created_at
        }
    
class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    streaks = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="habits")

    created_at = db.Column(
        db.Text(),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'streaks':self.streaks,
            'created_at': self.created_at
        }
    
class WorkSession(db.Model):
    __tablename__ = 'work_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    date = db.Column(db.String, nullable=False)
    minutes = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="work_sessions")