from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import *
from .models import User
from .views import load_user
from wtforms.fields import SelectField

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@bp.route('/index')
def admin_index():
    return render_template('admin/index.html')


@bp.route('/users')
def show_users():
    form = AdminEditForm()
    users = User.query.all()
    return render_template('admin/users_list.html', users = users, form=form)

@bp.route('/user/<int:id>/delete', methods=['GET', 'POST'])
def delete_user(id):
    user = load_user(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.show_users'))

@bp.route('/user/edit', methods=['POST'])
def edit_user():
    form = AdminEditForm()
    if form.validate_on_submit():
        user = load_user(form.user_id.data)

        if user is None:
            error = 'User not exist.'
            flash(error, 'danger')
            return redirect(url_for('admin.show_users'))

        user.name = form.name.data
        user.password = generate_password_hash(form.password.data)
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Edit user successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')

    return redirect(url_for('admin.show_users'))

