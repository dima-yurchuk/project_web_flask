from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
import sys
import os
from app import app
from app.forms import ContactForm, FormTaskCreate, FormTaskUpdate
from .models import Task
from . import db
import json
# app = Flask(__name__)
menu = {'Головна':'/', 'Коротка інформація':'/info', 'Мої досягнення':'/achievement', 'Contact':'/contact', 'FormTask':'/task'}
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
    tasks = Task.query.all()
    return render_template('tasks.html', title='Список завдань', menu=menu, tasks=tasks)


@app.route('/task/create', methods=["GET", "POST"])
def task_create():
    form = FormTaskCreate()
    if form.validate_on_submit():
        print(123)
        title = form.title.data
        description = form.description.data
        # created = form.created.data
        priority = form.priority.data
        # is_done = form.is_done.data
        task = Task(title=title, description=description, priority=priority)
        try:
            db.session.add(task)
            db.session.commit()
            flash('Data added in DB', 'success')
        except:
            db.session.rollback()
            flash('Error adding data in DB!', 'error')
        return redirect(url_for('task'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('task_create'))
    return render_template('task_create.html', menu=menu, form=form, title='Task create')

@app.route('/task/<int:id>', methods=["GET", "POST"])
def task_show(id):
    task = Task.query.get(id)
    return render_template('task_show.html', menu=menu, task=task)

@app.route('/task/<int:id>/update', methods=["GET", "POST"])
def task_update(id):
    form = FormTaskUpdate()
    task = Task.query.get_or_404(id)

    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.title.data = task.title
        form.description.data = task.description
        form.created.data = task.created
        form.priority.data = task.priority.name
        form.is_done.data = task.is_done
        return render_template('task_update.html', title='Task Update', form=form, menu=menu)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            task.title = form.title.data
            task.description = form.description.data
            task.created = form.created.data
            task.priority = form.priority.data
            task.is_done = form.is_done.data
            try:
                db.session.commit()
                flash('Task seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update task!', 'error')
            return redirect(url_for('task'))
        else:
            flash('Error when walidate!', 'error')
            return redirect(f'/task/{id}/update')

@app.route('/task/<int:id>/delete', methods=["GET", "POST"])
def task_delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task seccessfully deleted', 'success')
    except:
        flash('Error while delete task!', 'error')
    return redirect(url_for('task'))