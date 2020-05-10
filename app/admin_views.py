from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import *
from .models import User, Plant, Phase, Image
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

def delete_user_with_dependency(user):
    for image in user.images:
        db.session.delete(image)
    db.session.delete(user)
    db.session.commit()

@bp.route('/user/<int:id>/delete', methods=['GET', 'POST'])
def delete_user(id):
    user = load_user(id)
    if user is None:
        flash('User not exist!', 'danger')
        return  redirect(url_for('admin.show_users'))

    if user.is_admin:
        flash('Cannot delete admin!', 'danger')
        return redirect(url_for('admin.show_users'))

    delete_user_with_dependency(user)
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

@bp.route('/plants')
def show_plants():
    add_form = AddPlantForm()
    edit_form = EditPlantForm()
    add_phase_form = AddPhaseForm()
    plants = Plant.query.all()
    return render_template('admin/plants_list.html', plants = plants, add_form=add_form, edit_form=edit_form, add_phase_form=add_phase_form)

def load_plant(plant_id):
    return Plant.query.get(plant_id)

@bp.route('/plants/add', methods=['POST'])
def add_plant():
    form = AddPlantForm()
    if form.validate_on_submit():
        plant = Plant.query.filter_by(name=form.name.data).first()

        if plant is not None:
            error = 'Plant {} is already exist.'.format(form.name.data)
            flash(error, 'danger')
            return redirect(url_for('admin.show_plants'))

        p = Plant(name=form.name.data, number_of_days=form.number_of_days.data, timestamp=datetime.datetime.utcnow())
        db.session.add(p)
        db.session.commit()
        flash('Add plant successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')
    return redirect(url_for('admin.show_plants'))

@bp.route('/plant/edit', methods=['POST'])
def edit_plant():
    form = EditPlantForm()
    if form.validate_on_submit():
        plant = load_plant(form.plant_id.data)

        if plant is None:
            error = 'Plant not exist.'
            flash(error, 'danger')
            return redirect(url_for('admin.show_plants'))

        plant_test = Plant.query.filter_by(name=form.name.data).first()
        if plant_test and plant_test.id != plant.id:
            error = 'Plant {} is already exist.'.format(form.name.data)
            flash(error, 'danger')
            return redirect(url_for('admin.show_plants'))

        plant.name = form.name.data
        plant.number_of_days = form.number_of_days.data
        db.session.commit()
        flash('Edit plant successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')

    return redirect(url_for('admin.show_plants'))

def delete_plant_with_dependence(plant):
    for phase in plant.phases:
        for image in phase.images:
            db.session.delete(image)
        db.session.delete(phase)
    db.session.delete(plant)
    db.session.commit()

@bp.route('/plants/<int:id>/delete', methods=['GET', 'POST'])
def delete_plant(id):
    plant = load_plant(id)
    if plant is None:
        flash('Plant not exist!', 'danger')
        return  redirect(url_for('admin.show_plants'))

    delete_plant_with_dependence(plant)
    flash('Plant deleted successfully!', 'success')
    return redirect(url_for('admin.show_plants'))


@bp.route('/images')
def show_images():
    images = Image.query.all()
    return render_template('admin/images_list.html', images = images)

def load_image(image_id):
    return Image.query.get(image_id)

@bp.route('/images/<int:id>/delete', methods=['GET', 'POST'])
def delete_image(id):
    image = load_image(id)
    if image is None:
        flash('Image not exist!', 'danger')
        return  redirect(url_for('admin.show_images'))

    db.session.delete(image)
    db.session.commit()
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('admin.show_images'))

@bp.route('/phases/add', methods=['POST'])
def add_phase():
#     form = AddPhaseForm()
#     if form.validate_on_submit():
#         phase = Phase.query.filter_by(plant_id=form.plant_id.data).first()
#
#         if phase is None:
#             error = 'Plant {} is already exist.'.format(form.name.data)
#             flash(error, 'danger')
#             return redirect(url_for('admin.show_plants'))
#
#         p = Plant(name=form.name.data, number_of_days=form.number_of_days.data, timestamp=datetime.datetime.utcnow())
#         db.session.add(p)
#         db.session.commit()
#         flash('Add plant successfully!', 'success')
#     else:
#         flash('Invalid input!', 'danger')
    return redirect(url_for('admin.show_plants'))
