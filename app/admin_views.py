from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import *
from .models import User, Plant, Phase, Image, Feature
from .views import load_user, login_required, create_filename
from wtforms.fields import SelectField
from werkzeug.utils import secure_filename
import datetime
import unidecode
import os

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
            error = 'User "{}" is already registered.'.format(username)
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
    edit_phase_form = EditPhaseForm()
    plants = Plant.query.all()
    return render_template('admin/plants_list.html', plants = plants, add_form=add_form, edit_form=edit_form, add_phase_form=add_phase_form,
                           edit_phase_form=edit_phase_form)

def load_plant(plant_id):
    return Plant.query.get(plant_id)

@bp.route('/plants/add', methods=['POST'])
def add_plant():
    form = AddPlantForm()
    if form.validate_on_submit():
        plant = Plant.query.filter_by(name=form.name.data).first()

        if plant is not None:
            error = 'Plant "{}" is already exist.'.format(form.name.data)
            flash(error, 'danger')
            return redirect(url_for('admin.show_plants'))

        p = Plant(name=form.name.data, timestamp=datetime.datetime.utcnow())

        if form.avatar.data:
            file = form.avatar.data
            filename = secure_filename(file.filename)
            newname = create_filename(filename)
            file.save(os.path.join(app.config['PLANT_AVATAR_FOLDER'], newname))
            p.avatar = newname

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
            error = 'Plant "{}" is already exist.'.format(form.name.data)
            flash(error, 'danger')
            return redirect(url_for('admin.show_plants'))

        if form.avatar.data:
            file = form.avatar.data
            filename = secure_filename(file.filename)
            newname = create_filename(filename)
            file.save(os.path.join(app.config['PLANT_AVATAR_FOLDER'], newname))
            plant.avatar = newname

        plant.name = form.name.data
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

def load_phase(phase_id):
    return Phase.query.get(phase_id)

@bp.route('/phases/add', methods=['POST'])
def add_phase():
    form = AddPhaseForm()
    if form.validate_on_submit():
        plant = Plant.query.filter_by(id=form.plant_id.data).first()

        if plant is None:
            flash('Plant not exist!', 'danger')
            return redirect(url_for('admin.show_plants'))

        for plant_phase in plant.phases:
            if form.order.data == plant_phase.order:
                error = 'Order {} is already exist in plant "{}".'.format(form.order.data, plant.name)
                flash(error, 'danger')
                return redirect(url_for('admin.show_plants'))

        phase = Phase(name=form.name.data, number_of_days=form.number_of_days.data, order=form.order.data, plant_id=form.plant_id.data, timestamp=datetime.datetime.utcnow())
        db.session.add(phase)
        db.session.commit()
        flash('Add phase successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')
    return redirect(url_for('admin.show_plants'))

@bp.route('/phases/edit', methods=['POST'])
def edit_phase():
    form = EditPhaseForm()
    if form.validate_on_submit():
        phase = load_phase(form.phase_id.data)

        if phase is None:
            flash('Phase not exist!', 'danger')
            return redirect(url_for('admin.show_plants'))

        for plant_phase in phase.plant.phases:
            if form.order.data == plant_phase.order and phase.id!=plant_phase.id:
                error = 'Order {} is already exist in plant "{}".'.format(form.order.data, phase.plant.name)
                flash(error, 'danger')
                return redirect(url_for('admin.show_plants'))

        phase.name = form.name.data
        phase.order = form.order.data
        phase.number_of_days = form.number_of_days.data
        db.session.commit()
        flash('Edit phase successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')
    return redirect(url_for('admin.show_plants'))

def delete_phase_with_dependence(phase):
    for image in phase.images:
        db.session.delete(image)
    db.session.delete(phase)
    db.session.commit()

@bp.route('/phases/<int:id>/delete', methods=['GET', 'POST'])
def delete_phase(id):
    phase = load_phase(id)
    if phase is None:
        flash('Phase not exist!', 'danger')
        return  redirect(url_for('admin.show_plants'))

    delete_phase_with_dependence(phase)
    flash('Phase deleted successfully!', 'success')
    return redirect(url_for('admin.show_plants'))

@bp.route('/features')
def show_features():
    form = AddFeatureForm()
    features = Feature.query.all()
    return render_template('admin/features_list.html', features=features, form=form)

def convert2code(text):
    tx = unidecode.unidecode(text)
    return tx.replace(' ', '').lower()

@bp.route('/features/add', methods=['POST'])
def add_feature():
    form = AddFeatureForm()
    if form.validate_on_submit():
        feature_test = Feature.query.filter_by(code=convert2code(form.name.data)).first()
        if feature_test is not None:
            flash('Feature "{}" is already exist.'.format(form.name.data), 'danger')
            return redirect(url_for('admin.show_features'))

        feature = Feature(name=form.name.data, code=convert2code(form.name.data), timestamp=datetime.datetime.utcnow())
        db.session.add(feature)
        db.session.commit()
        flash('Add feature successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')
    return redirect(url_for('admin.show_features'))

def load_feature(feature_id):
    return Feature.query.get(feature_id)

@bp.route('/features/<int:id>/delete', methods=['GET', 'POST'])
def delete_feature(id):
    feature = load_feature(id)
    if feature is None:
        flash('Feature not exist!', 'danger')
        return  redirect(url_for('admin.show_features'))

    db.session.delete(feature)
    db.session.commit()
    flash('Feature deleted successfully!', 'success')
    return redirect(url_for('admin.show_features'))

@bp.route('/phase_detail/<int:id>')
def show_phase_detail(id):
    add_phase_feature_form = AddPhaseFeatureForm()
    phase = load_phase(id)
    if phase is None:
        flash('Phase not exist!', 'danger')
        return redirect(url_for('admin.show_plants'))

    features = Feature.query.all()
    features_list = [(feature.id, feature.name) for feature in features if feature not in phase.features]
    add_phase_feature_form.feature_id.choices = features_list
    return render_template('admin/phase_detail.html', phase=phase, add_phase_feature_form=add_phase_feature_form)

@bp.route('/phase/<int:id>/add_feature', methods=['POST'])
def add_feature2phase(id):
    add_phase_feature_form = AddPhaseFeatureForm()
    phase = load_phase(id)
    if phase is None:
        flash('Phase not exist!', 'danger')
        return redirect(url_for('admin.show_plants'))

    features = Feature.query.all()
    features_list = [(feature.id, feature.name) for feature in features if feature not in phase.features]
    add_phase_feature_form.feature_id.choices = features_list
    if add_phase_feature_form.validate_on_submit():
        feature = load_feature(add_phase_feature_form.feature_id.data)
        if feature is None:
            flash('Feature not exist!', 'danger')
            return redirect(url_for('admin.show_phase_detail', id=id))

        if feature in phase.features:
            flash('Feature "{}" is already exist in phase "{}".'.format(feature.name, phase.name), 'danger')
            return redirect(url_for('admin.show_phase_detail', id=id))

        phase.features.append(feature)
        db.session.commit()
        flash('Add successfully!', 'success')
    else:
        flash('Invalid input!', 'danger')

    return redirect(url_for('admin.show_phase_detail', id=id))

@bp.route('/phase/<int:phase_id>/delete_feature/<int:feature_id>', methods=['GET', 'POST'])
def delete_featurefromphase(phase_id, feature_id):
    phase = load_phase(phase_id)
    if phase is None:
        flash('Phase not exist!', 'danger')
        return redirect(url_for('admin.show_plants'))

    feature = load_feature(feature_id)
    if feature is None:
        flash('Feature not exist!', 'danger')
        return redirect(url_for('admin.show_phase_detail', id=phase_id))

    if feature not in phase.features:
        flash('feature "{}" not in phase "{}"!'.format(feature.name, phase.name), 'danger')
        return redirect(url_for('admin.show_phase_detail', id=phase_id))

    phase.features.remove(feature)
    db.session.commit()
    flash('Delete feature "{}" from phase "{}" successfully!'.format(feature.name, phase.name), 'success')

    return redirect(url_for('admin.show_phase_detail', id=phase_id))