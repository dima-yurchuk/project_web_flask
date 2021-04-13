from flask import render_template, request, redirect, url_for, flash
import os, secrets
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from datetime import datetime

from app.profile import user_bp
from app import bcrypt
from .form import  RegistrationForm, LoginForm, UpdateAccountForm
from .models import User
from app import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

def save_picture(form_picture):
    rendom_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rendom_hex + f_ext
    picture_path = os.path.join(user_bp.root_path, '../static/profile_pics', picture_fn)
    # form_picture.save(picture_path)
    # return  picture_fn
    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Account cereated for {form.username.data}!', category='success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'danger')
        return redirect(url_for('user_bp_in.login'))
    return render_template('register.html', form=form, title='Register')

@user_bp.route('/login', methods=['GET', 'POST'])
@user_bp.route('/login2', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('task_bp_in.task'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_in_db = User.query.filter(User.email==email).first()
        if user_in_db and user_in_db.veryfy_password(password):
            login_user(user_in_db, remember=form.remember.data)
            # del menu['Login']
            # menu['Профіль'] = '/account'
            # menu['Вихід'] = '/logout'
            flash('Ви успішно ввійшли!', category='success')
            next = request.args.get('next')
            print('next post', next)
            # from werkzeug.urls import url_parse
            # next_page = request.args.get('next')
            # if not next_page or url_parse(next_page).netloc != '':
            #     next_page = url_for('index')
            #
            # if not is_safe_url(next, {'127.0.0.1:5000'}):
            #     return abort(400)
            #
            # if next:
            #     return redirect(next)
            return redirect(url_for('task_bp_in.task'))
        else:
            flash('Неправильні дані!', category='danger')
    return render_template('login.html', form=form, title='Login')

@user_bp.route('/logout')
def logout():
    # del menu['Профіль']
    # del menu['Вихід']
    # menu['Login'] = '/login'
    logout_user()
    flash('Ви вийшли зі свого акаунту!', 'info')
    return redirect(url_for("task_bp_in.task"))

@user_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    user_img = url_for('static', filename = 'profile_pics/'+current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.password.data:
            if current_user.veryfy_password(form.old_password.data):
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            else:
                flash('Incorrect old password!', 'danger')
                return redirect(url_for('user_bp_in.account'))
        try:
            db.session.commit()
            flash('User seccessfully updated', 'info')
            return redirect(url_for('user_bp_in.account'))
        except:
            db.session.rollback()
            flash('Error while update user!', 'danger')
            return redirect(url_for('user_bp_in.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('account.html', title='Account', user_img=user_img, form=form)

@user_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response