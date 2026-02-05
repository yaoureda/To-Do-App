from .config import web_bp
from flask_login import login_required, logout_user
from flask import redirect, url_for

@web_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))