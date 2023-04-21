from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from database import User, db

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            session['user_id'] = user.id
            return redirect(url_for('main_window.main_view'))
        else:
            flash('Incorrect username or password.')
            return render_template("login.html", error="用户名或密码错误，请重试")

    return render_template('login.html')

