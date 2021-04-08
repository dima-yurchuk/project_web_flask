from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
import sys
import os
from os import abort
from app import app, bcrypt
from app.forms import ContactForm, FormTaskCreate, FormTaskUpdate,CategoryCreate, EmployeeCreate, RegistrationForm,\
    LoginForm, UpdateAccountForm, ChangePassword
from .models import Task, Category, Employee, User
from . import db
import json
from sqlalchemy import case
from flask_login import login_user, current_user, logout_user, login_required
from is_safe_url import is_safe_url
import secrets
from PIL import Image



def save_picture(form_picture):
    rendom_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rendom_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # form_picture.save(picture_path)
    # return  picture_fn
    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# app = Flask(__name__)
menu = {'Головна':'/', 'Коротка інформація':'/info', 'Мої досягнення':'/achievement', 'Contact':'/contact', 'FormTask':'/task', 'Login':'/login'}
today = date.today()
age = today.year - 2001 - ((today.month, today.day) < (4, 14))


@app.route('/')
def index():
    return render_template('index.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))


@app.route('/info')
def info():
    return render_template('info.html', menu=menu,age=age, month=today.month, day=today.day)


@app.route('/achievement')
def achievement():
    return render_template('achievement.html', menu=menu)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    cookie_name = session.get("name")
    cookie_email = session.get("email")
    print(cookie_email,cookie_name)
    if request.method == 'POST':
        if cookie_name is None and cookie_email is None: # якщо кукі не встановлено, тобто ми перший раз відкрили сторінку
            if form.validate_on_submit():
                name = form.name.data
                email = form.email.data
                body = form.body.data
                session['name'] = name
                session['email'] = email
                with open('data.json', 'a') as outfile:
                    json_string = json.dumps({'name': session.get("name"), 'email': session.get("email"), 'body': body})
                    json.dump(json_string, outfile)
                    outfile.write('\n')
                flash(message='Повідомлення надіслано успішно!')
                return redirect(url_for('contact'))
            else:
                flash(message='Помилка відправки повідомлення!')
        else: # якщо вхід на сторіку здійснено повторно
            form.name.data = cookie_name # встановлюємо значення для форми name та email
            form.email.data = cookie_email
            if form.validate_on_submit():
                body = form.body.data
                with open('data.json', 'a') as outfile:
                    json.dump({'name': session.get("name"), 'email': session.get("email"), 'body': body}, outfile)
                    outfile.write('\n')
                flash(message='Повідомлення надіслано успішно!')
                return redirect(url_for('contact'))
            else:
                flash(message='Помилка відправки повідомлення!')
    return render_template('contact_form.html', menu=menu, form=form, cookie_name=session.get("name"), cookie_email=session.get("email"))


@app.route('/task', methods=["GET", "POST"])
def task():
    tasks = Task.query.order_by(case(value=Task.priority, whens={'low':2, 'medium':1, 'high':0}), Task.created).all()
    return render_template('tasks.html', title='Список завдань', menu=menu, tasks=tasks)

@app.route('/category', methods=["GET", "POST"])
def category():
    categories = Category.query.all()
    return render_template('categories.html', title='Список категорій', menu=menu,  categories=categories)

@app.route('/employee', methods=["GET", "POST"])
def employee():
    employers = Employee.query.all()
    return render_template('employers.html', title='Список категорій', menu=menu,  employers=employers)


@app.route('/task/create', methods=["GET", "POST"])
def task_create():
    categories = Category.query.all()
    form = FormTaskCreate.new()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        # created = form.created.data
        priority = form.priority.data
        category_id = form.category.data
        # is_done = form.is_done.data
        category_id=db.session.query(Category.id).filter(Category.id==category_id)
        # category_id = db.session.query(Category.id).filter(Category.name == category_name).all()[0][0]
        print(category_id)
        employers = form.employee.data
        print(employers)
        task = Task(title=title, description=description, priority=priority, category_id=category_id)
        print(task)
        try:
            for employee in employers:
                task.employee_backref.append(Employee.query.get_or_404(employee))
            db.session.add(task)
            db.session.commit()
            flash('Data added in DB', 'success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'danger')
        return redirect(url_for('task'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('task_create'))
    return render_template('task_create.html', menu=menu, form=form, title='Task create')

@app.route('/category/create', methods=["GET", "POST"])
def category_create():
    form = CategoryCreate()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        try:
            db.session.add(category)
            db.session.commit()
            flash('Data added in DB', 'success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'danger')
        return redirect(url_for('task'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('category_create'))
    return render_template('category_create.html', menu=menu, form=form, title='Category create')

@app.route('/employee/create', methods=["GET", "POST"])
def employee_create():
    form = EmployeeCreate()
    if form.validate_on_submit():
        name = form.name.data
        employee = Employee(name=name, count_of_completed_tasks=0)
        print(employee)
        try:
            db.session.add(employee)
            db.session.commit()
            print(12345)
            flash('Data added in DB', 'success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'danger')
        return redirect(url_for('employee'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('employee_create'))
    return render_template('employee_create.html', menu=menu, form=form, title='Employee create')

@app.route('/task/<int:id>', methods=["GET", "POST"])
def task_show(id):
    task = Task.query.get_or_404(id)
    # print(task[0][0].employee_backref)
    # print(task[0])
    return render_template('task_show.html', menu=menu, task=task)

@app.route('/category/<int:id>', methods=["GET", "POST"])
def category_show(id):
    category = Category.query.get(id)
    return render_template('category_show.html', menu=menu, category=category)

@app.route('/employee/<int:id>', methods=["GET", "POST"])
def employee_show(id):
    employee = Employee.query.get_or_404(id)
    # tasks = db.session.query(Task).filter(Task.employee_backref.contains(employee)).all()
    tasks = db.session.query(Task).filter(Task.employee_backref.contains(employee))
    print(tasks)
    return render_template('employee_show.html', menu=menu, employee=employee, tasks=tasks)

@app.route('/task/<int:id>/update', methods=["GET", "POST"])
def task_update(id):
    form = FormTaskUpdate.new()
    task = Task.query.get_or_404(id)
    is_done_first = task.is_done
    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.title.data = task.title
        form.description.data = task.description
        form.created.data = task.created
        form.priority.data = task.priority.name
        form.is_done.data = task.is_done
        form.category.data = task.category_backref.id
        form.employee.data = [empl.id for empl in task.employee_backref]
        return render_template('task_update.html', title='Task Update', form=form, menu=menu)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            task.title = form.title.data
            task.description = form.description.data
            task.created = form.created.data
            task.priority = form.priority.data
            task.is_done = form.is_done.data
            task.category_id = db.session.query(Category.id).filter(Category.id==form.category.data)
            employers = form.employee.data
            task.employee_backref.clear()
            for employee in employers:
                empl = Employee.query.get_or_404(employee)
                if is_done_first and task.is_done==False:
                    empl.count_of_completed_tasks = empl.count_of_completed_tasks - 1
                elif is_done_first==False and task.is_done:
                    empl.count_of_completed_tasks = empl.count_of_completed_tasks + 1
                task.employee_backref.append(Employee.query.get_or_404(employee))
            try:
                db.session.commit()
                flash('Task seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update task!', 'danger')
            return redirect(url_for('task'))
        else:
            flash('Error when walidate!', 'danger')
            return redirect(f'/task/{id}/update')

@app.route('/category/<int:id>/update', methods=["GET", "POST"])
def category_update(id):
    form = CategoryCreate()
    category = Category.query.get_or_404(id)

    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.name.data = category.name
        return render_template('category_update.html', title='Category Update', form=form, menu=menu)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            category.name = form.name.data
            try:
                db.session.commit()
                flash('Category seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update category!', 'danger')
            return redirect(url_for('task'))
        else:
            flash('Error when walidate!', 'danger')
            return redirect(f'/category/{id}/update')


@app.route('/employee/<int:id>/update', methods=["GET", "POST"])
def employee_update(id):
    form = EmployeeCreate()
    employee = Employee.query.get_or_404(id)

    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.name.data = employee.name
        return render_template('employee_update.html', title='Employee Update', form=form, menu=menu)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            employee.name = form.name.data
            try:
                db.session.commit()
                flash('Employee seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update employee!', 'danger')
            return redirect(url_for('employee'))
        else:
            flash('Error when walidate!', 'danger')
            return redirect(f'/employee/{id}/update')


@app.route('/task/<int:id>/delete', methods=["GET", "POST"])
def task_delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task seccessfully deleted', 'success')
    except:
        flash('Error while delete task!', 'danger')
    return redirect(url_for('task'))

@app.route('/category/<int:id>/delete', methods=["GET", "POST"])
def category_delete(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category seccessfully deleted', 'success')
    except:
        flash('Error while category deleted!', 'danger')
    return redirect(url_for('task'))

@app.route('/employee/<int:id>/delete', methods=["GET", "POST"])
def employee_delete(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee seccessfully deleted', 'success')
    except:
        flash('Error while employee deleted!', 'danger')
    return redirect(url_for('employee'))

@app.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register', menu=menu)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('task'))
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
            return redirect(url_for('task'))
        else:
            flash('Неправильні дані!', category='danger')
    return render_template('login.html', menu=menu, form=form, title='Login')

@app.route('/logout')
def logout():
    # del menu['Профіль']
    # del menu['Вихід']
    # menu['Login'] = '/login'
    logout_user()
    flash('Ви вийшли зі свого акаунту!', 'info')
    return redirect(url_for("task"))

@app.route("/account", methods=['GET', 'POST'])
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
                return redirect(url_for('account'))
        try:
            db.session.commit()
            flash('User seccessfully updated', 'info')
            return redirect(url_for('account'))
        except:
            db.session.rollback()
            flash('Error while update user!', 'danger')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('account.html',  menu=menu, title='Account', user_img=user_img, form=form)

@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    user_in_db = User.query.filter(User.email == current_user.email).first()
    user_img = url_for('static', filename = 'profile_pics/'+current_user.image_file)
    if form.validate_on_submit():
        if user_in_db.veryfy_password(form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            try:
                db.session.commit()
                flash('Password seccessfully updated', 'info')
                return redirect(url_for('account'))
            except:
                db.session.rollback()
                flash('Error while update password!', 'danger')
                return redirect(url_for('account'))
        else:
            flash('Incorrect old password!', 'danger')
            return redirect(url_for('change_password'))
    return render_template('change_password.html',  menu=menu, title='Account', user_img=user_img, form=form)


@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response