from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import *
from .models import User
from .views import load_user, login_required
from wtforms.fields import SelectField
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def check_admin():
    if g.user.is_admin == 0:
        abort(401)

@bp.route('/')
@bp.route('/index')
def admin_index():
    return render_template('admin/index.html')


@bp.route('/users')
def show_users():
    add_form = AdminAddForm()
    edit_form = AdminEditForm()
    users = User.query.all()
    return render_template('admin/users_list.html', users = users, add_form=add_form, edit_form=edit_form)

@bp.route('/user/<int:id>/delete', methods=['GET', 'POST'])
def delete_user(id):
    user = load_user(id)
    if user.is_admin:
        flash('Cannot delete admin!', 'danger')
        return redirect(url_for('admin.show_users'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.show_users'))

@bp.route('/users/add', methods=['POST'])
def add_user():
    form = AdminAddForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        address = form.address.data
        phone_number = form.phone_number.data
        is_admin = form.is_admin.data
        user = User.query.filter_by(username=username).first()

        if user is not None:
            error = 'User {} is already registered.'.format(username)
            flash(error, 'danger')
            return redirect(url_for('admin.show_users'))

        u = User(username=username, password=generate_password_hash(password), name=name, address=address, phone_number=phone_number, is_admin=is_admin, timestamp=datetime.datetime.utcnow())
        db.session.add(u)
        db.session.commit()
        flash('Add user successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')

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

        if user.is_admin:
            flash('Cannot edit admin!', 'danger')
            return redirect(url_for('admin.show_users'))

        user.name = form.name.data
        user.address = form.address.data
        user.phone_number = form.phone_number.data

        if form.edit_password.data and form.password.data:
            user.password = generate_password_hash(form.password.data)

        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Edit user successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')

    return redirect(url_for('admin.show_users'))

