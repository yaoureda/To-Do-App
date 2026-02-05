from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from .database.database import db, init_database
from .database.models import User
from .api.config import api_bp
from .web.config import web_bp
from flask_login import LoginManager
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-key')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database', 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) 
with app.app_context():
    init_database()

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)

login_manager = LoginManager()
login_manager.login_view = 'web.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    return user

if __name__ == "__main__":
    app.run(debug=False)