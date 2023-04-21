from flask import Blueprint, redirect, url_for, session

bp = Blueprint('logout', __name__, url_prefix='/logout')

@bp.route('/')
def logout():
    session.clear()
    return redirect(url_for('login.login'))
