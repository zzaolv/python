from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from database import User, db
from auth import login_required

bp = Blueprint('user_management', __name__, url_prefix='/user_management')

@bp.route('/add_user', methods=('POST',))
def add_user():
    if 'is_admin' in session and session['is_admin']:
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        position = request.form['position']
        is_admin = 'is_admin' in request.form

        user = User(username=username, gender=gender, position=position, is_admin=is_admin)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('User added successfully.')
        return redirect(url_for('main_window.main'))
    else:
        flash('Only admin can add users.')
        return redirect(url_for('main_window.main'))
@bp.route('/add_user_form', methods=('GET',))
@login_required
def add_user_form():
    return render_template('add_user.html')

@bp.route('/list_users', methods=('GET',))
@login_required
def list_users():
    if 'is_admin' in session and session['is_admin']:
        users = User.query.all()
        return render_template('list_users.html', users=users)
    else:
        flash('Only admin can view and delete users.')
        return redirect(url_for('main_window.main'))

@bp.route('/delete_user/<int:user_id>', methods=('POST',))
@login_required
def delete_user(user_id):
    if 'is_admin' in session and session['is_admin']:
        user = User.query.get(user_id)
        if user:
            if not user.is_admin:  # 确保要删除的用户不是管理员
                db.session.delete(user)
                db.session.commit()
                flash('User deleted successfully.')
            else:
                flash('Admin users cannot be deleted.')
        else:
            flash('User not found.')
    else:
        flash('Only admin can delete users.')
    return redirect(url_for('user_management.list_users'))
