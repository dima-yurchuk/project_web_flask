from flask import render_template, request, redirect, url_for, flash
import os, secrets
from os import abort
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from datetime import datetime

from app.profile import user_bp
from app import bcrypt
from .form import  RegistrationForm, LoginForm, UpdateAccountForm, AdminUserCreateForm, AdminUserUpdateForm
from .models import User
from app import db, login_manager
from functools import wraps



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


from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length, Email
from flask_admin.form import rules
from wtforms import widgets, TextAreaField
class CustomView(BaseView):
    @expose('/')
    # @login_required
    # @has_role('admin')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    # @login_required
    # @has_role('admin')
    def second_page(self):
        return self.render('admin/second_page.html')

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field,**kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class UserModelView(ModelView):
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'admin')
    column_list = ('username', 'email', 'admin', )
    column_exclude_list = ('pwdhash',)
    form_excluded_columns = ('pwdhash',)
    # form_edit_rules = ('username', 'admin')
    # form_create_rules = ('username', 'password', 'admin')

    form_edit_rules = (
        'username', 'email', 'about_me', 'admin',
        rules.Header('Reset Password'),
        'new_password', 'confirm'
    )
    form_create_rules = (
        'username', 'email', 'admin', 'password'
    )

    form_overrides = dict(about_me=CKTextAreaField)
    create_template = 'edit.html'
    edit_template = 'edit.html'

    def scaffold_form(self):
        form_class = super(UserModelView, self).scaffold_form()
        form_class.password= PasswordField(
            'Password',
            validators=[Length(min=8,
                               message='Поле повинно бути довжиною більше 8 символів!'),
                        DataRequired(message="Це поле є обов'язковим!")]
        )
        form_class.new_password = PasswordField('New Password')
        form_class.confirm = PasswordField('Confirm New Password')
        return form_class

    def create_model(self, form):
        model = self.model(
            form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            form.admin.data
        )
        # form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    def update_model(self, form, model):
        form.populate_obj(model)
        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash('Passwords must match')
                return
            model.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, *kwargs):
        return redirect(url_for('index', next=request.url))

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, *kwargs):
        return redirect(url_for('index', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated  and current_user.admin

    def inaccessible_callback(self, name, *kwargs):
        return redirect(url_for('index', next=request.url))



def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # admin = False
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



@user_bp.route('/administrator')
@login_required
@admin_login_required
def home_admin():
  return render_template('admin-home.html', title='Home')

@user_bp.route('/administrator/users-list')
@login_required
@admin_login_required
def users_list_admin():
    users = User.query.all()
    return render_template('users-list-admin.html', title='List users', users=users)

@user_bp.route('/administrator/create-user',  methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_create_admin():
    form = AdminUserCreateForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        admin = form.admin.data
        user = User(username=username, email=email, password=password, admin=admin)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Data added in DB', 'success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'danger')
        return redirect(url_for('user_bp_in.users_list_admin'))
    # elif request.method == 'POST':
    #     flash('Unseccess!', 'error')
    #     return redirect(url_for('user_bp_in.user_create_admin'))
    return render_template('user-create-admin.html', title='Create user', form=form)


@user_bp.route('/administrator/update-user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_update_admin(id):
    form = AdminUserUpdateForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.admin = form.admin.data
            try:
                db.session.commit()
                flash('User seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update user!', 'danger')
            return redirect(url_for('user_bp_in.users_list_admin'))
    else:
        form.username.data = user.username
        form.email.data = user.email
        form.admin.data = user.admin
        return render_template('user-update-admin.html', title='Update user', form=form, user=user)





@user_bp.route('/administrator/delete-user/<int:id>')
@login_required
@admin_login_required
def user_delete_admin(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User seccessfully deleted', 'success')
    except:
        flash('Error while user deleted!', 'danger')
    return redirect(url_for('.home_admin'))


@user_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response
