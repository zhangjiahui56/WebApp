from flask import render_template, flash, redirect, session, url_for, request, g, abort, send_from_directory, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager, model
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime
import os
import functools
import zipfile
import shutil
from .forms import *
from .models import User, Plant, Phase, Image
from leaf_area import calculate_leaf_area
from length_leaf import calculate_max_length_leaf, calculate_average_length_leaf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.is_admin == 0:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

def check_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        address = form.address.data
        phone_number = form.phone_number.data
        user = User.query.filter_by(username=form.username.data).first()
        error = None

        if user is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            u = User(username=username, password=generate_password_hash(password), name=name, address=address, phone_number=phone_number, timestamp=datetime.datetime.utcnow())
            db.session.add(u)
            db.session.commit()
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))
        flash(error, 'danger')

    return render_template('register.html', form = form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
@check_login
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, form.password.data):
            error = 'Incorrect password.'

        if error is None:
            login_user(user, remember=form.remember_me.data)
            # flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash(error, 'danger')
    return render_template('login.html', form=form)

@app.before_request
def load_logged_in_user():
    if current_user.is_authenticated:
        g.user = load_user(current_user.get_id())
    else:
        g.user = None

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

""" upload image """

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

import random, string

def randomword(length):
   letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))

def time_now():
    return datetime.datetime.now().strftime('%m%d%Y%H%M%S%f')

def create_filename(filename):
    name = filename.rsplit('.', 1)[0]
    file_format = filename.rsplit('.', 1)[1]
    return time_now() + '_' + randomword(10) + '_' + name + '.' + file_format

def load_plant(plant_id):
    return Plant.query.get(plant_id)

def load_phase(phase_id):
    return Phase.query.get(phase_id)

@app.route('/plants/<int:plant_id>/images', methods=['GET', 'POST'])
@login_required
def upload_file(plant_id):
    plant = load_plant(plant_id)
    if plant is None:
        abort(404)
    upload_form = UploadImageForm()
    phases_list = [(phase.id, phase.name) for phase in plant.phases.order_by("order")]
    upload_form.phase_id.choices = phases_list
    if upload_form.validate_on_submit():

        phase = load_phase(upload_form.phase_id.data)
        if phase is None:
            flash("Phase not exist!", 'danger')
            return redirect(url_for('upload_file', plant_id=plant.id))

        file = upload_form.image.data
        filename = secure_filename(file.filename)
        # leaf_pred = leaf_predict(file)
        newname = create_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newname))

        img = Image(filename=newname, user_id=g.user.id, phase_id=upload_form.phase_id.data, timestamp=datetime.datetime.utcnow())
        db.session.add(img)
        db.session.commit()
        flash('Upload successfully!', 'success')
        return redirect(url_for('show_results', plant_id=plant.id, phase_order=phase.order, filename=newname))

    return render_template('upload_images.html', upload_form=upload_form, plant=plant)

import numpy as np
def leaf_predict(np_image):
    import keras.backend.tensorflow_backend as tb
    tb._SYMBOLIC_SCOPE.value = True
    from keras.applications.resnet50 import preprocess_input

    image = preprocess_input(np_image)
    predict = model.predict(np.expand_dims(image, axis=0))
    return predict[0][0]

def calculate_phase_1(filename):
    from LeafCounting.utils import load_image
    image = load_image(filename)
    leaf_count = leaf_predict(image)
    # leaf_count = 0
    max_length = calculate_max_length_leaf(image)
    average_length = calculate_average_length_leaf(image)

    return (leaf_count, max_length, average_length)


def calculate_phase_2(filename):
    area = calculate_leaf_area(filename)

    return area

@app.route('/plants/<int:plant_id>/<int:phase_order>/images/results/<filename>')
@login_required
def show_results(plant_id, phase_order, filename):
    plant = load_plant(plant_id)
    if plant is None:
        abort(404)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if phase_order == 1:
        leaf_count, max_length, average_length = calculate_phase_1(file_path)
        return render_template('results.html', plant=plant, phase_order=phase_order, filename=filename, leaf_count=leaf_count, max_length=max_length, average_length=average_length)

    area = calculate_phase_2(file_path)
    return render_template('results.html', plant=plant, phase_order=phase_order, filename=filename, area=area)


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required

def edit_profile(id):
    if g.user.id != id:
        abort(401)

    form = EditProfileForm()
    user = load_user(id)
    if user is None:
        flash('User not exist.', 'danger')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user.name = form.name.data
        user.address = form.address.data
        user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Edit profile successfully!', 'success')
        return redirect(url_for('edit_profile', id=user.id))

    return render_template('profile.html', form=form, user=user)

@app.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    if g.user.id != id:
        abort(401)

    form = ChangePassword()
    user = load_user(id)
    if user is None:
        flash('User not exist.', 'danger')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        if not check_password_hash(user.password, form.old_password.data):
            flash('Password is not correct', 'danger')
            return redirect(url_for('change_password', id=user.id))
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Change password successfully!', 'success')
        return redirect(url_for('change_password', id=user.id))

    return render_template('change_password.html', form=form, user=user)

@app.route('/choose_plants', methods=['GET'])
@login_required
def choose_plants():
    plants = Plant.query.all()
    return render_template('choose_plants.html', plants=plants)

@app.route('/choose_plants_multiple', methods=['GET'])
@login_required
def choose_plants_multiple():
    plants = Plant.query.all()
    return render_template('choose_plants_multiple.html', plants=plants)


def get_dir_name(zip_ref):
    return list(set([os.path.dirname(name) for name in zip_ref.namelist()]))[0]

def process_multi_images(zip_ref, newname):
    dir_name = get_dir_name(zip_ref)
    dir_path = os.path.join(app.config['EXTRACT_ZIP_FOLDER'], dir_name)
    images_path = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    leaf_areas = [calculate_leaf_area(f) for f in images_path]
    # plt.xlim(0, 30)
    plt.xlabel("Images")
    plt.ylabel("Percent of Image")
    plt.xticks([i for i in range(len(leaf_areas))])
    plt.tick_params(labelsize=10)
    plt.ylim(0, 1)
    plt.plot([i for i in range(len(leaf_areas))], leaf_areas)
    result_filename = os.path.splitext(newname)[0] + '.png'
    plt.savefig(os.path.join(app.config['GRAPH_IMAGES_FOLDER'], result_filename))
    plt.close()
    return result_filename

@app.route('/plants/<int:plant_id>/zip', methods=['GET', 'POST'])
@login_required
def upload_zip(plant_id):
    plant = load_plant(plant_id)
    if plant is None:
        abort(404)

    upload_form = UploadZipForm()
    phases_list = [(phase.id, phase.name) for phase in plant.phases.order_by("order")]
    upload_form.phase_id.choices = phases_list
    if upload_form.validate_on_submit():

        phase = load_phase(upload_form.phase_id.data)
        if phase is None:
            flash("Phase not exist!", 'danger')
            return redirect(url_for('upload_zip', plant_id=plant.id))

        zip_file = upload_form.zip_file.data
        filename = secure_filename(zip_file.filename)

        newname = create_filename(filename)
        zip_file.save(os.path.join(app.config['UPLOAD_ZIP_FOLDER'], newname))

        zip_ref = zipfile.ZipFile(os.path.join(app.config['UPLOAD_ZIP_FOLDER'], newname), 'r')
        zip_ref.extractall(app.config['EXTRACT_ZIP_FOLDER'])
        zip_ref.close()

        # process images in zip file
        result_graph = process_multi_images(zip_ref, newname)
        # end process

        shutil.rmtree(os.path.join(app.config['EXTRACT_ZIP_FOLDER'], get_dir_name(zip_ref)))

        flash('Upload successfully!', 'success')
        return redirect(url_for('show_graph_result', plant_id=plant.id, result_graph=result_graph))

    return render_template('upload_zip.html', upload_form=upload_form, plant=plant)

@app.route('/plants/<int:plant_id>/zip/results/<result_graph>', methods=['GET'])
@login_required
def show_graph_result(plant_id, result_graph):
    plant = load_plant(plant_id)
    if plant is None:
        abort(404)
    return render_template('show_graph_result.html', plant=plant, result_graph=result_graph)

@app.route('/download_graph/<result_graph>')
@login_required
def download_graph(result_graph):
    return send_from_directory(app.config['DOWNLOAD_IMAGES'], filename=result_graph)