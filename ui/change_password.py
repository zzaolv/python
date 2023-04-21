from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import User, db
from auth import login_required

bp = Blueprint('change_password', __name__, url_prefix='/change_password')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user_id = session['user_id']
        user = User.query.get(user_id)

        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully.')
                return redirect(url_for('main_window.main'))
            else:
                flash('New password and confirmation do not match.')
        else:
            flash('Current password is incorrect.')

    return render_template('change_password.html')
