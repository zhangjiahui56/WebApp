from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime
import os
import functools
from .forms import *
from .models import User

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

import numpy as np
# def leaf_predict(image):
#     image = preprocess_image(image)
#     predict = model.predict(np.expand_dims(image, axis=0))
#     return predict

def time_now():
    return datetime.datetime.now().strftime('%m%d%Y%H%M%S%f')

def create_filename(filename):
    name = filename.rsplit('.', 1)[0]
    file_format = filename.rsplit('.', 1)[1]
    return time_now() + '_' + name + '.' + file_format

@app.route('/images', methods=['GET'])
@login_required
def upload_file():
    return render_template('upload_images.html')

@app.route('/images/results', methods=['POST'])

def uploaded_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('upload_file'))
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('upload_file'))
    if allowed_file(file.filename) == 0:
        flash('Invalid file, please choose png, jpg or jpeg file', 'danger')
        return redirect(url_for('upload_file'))
    if file:
        filename = secure_filename(file.filename)
        # leaf_pred = leaf_predict(file)
        newname = create_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newname))
        return render_template('results.html', image_link=newname)

    return redirect(url_for('upload_file'))

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
        flash('Edit user successfully!', 'success')
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
