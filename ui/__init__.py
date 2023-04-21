from flask import Blueprint, render_template, session
from database import User

ui_bp = Blueprint('ui', __name__, url_prefix='/ui')

@ui_bp.context_processor
def add_user_to_context():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        user = None
    return {'user': user}
