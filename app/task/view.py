from flask import render_template, request, redirect, url_for, flash


from app.task import task_bp
from .form import FormTaskCreate, FormTaskUpdate, CategoryCreate, EmployeeCreate
from .models import  Task, Category, Employee
from app import db
from sqlalchemy import case


@task_bp.route('/task', methods=["GET", "POST"])
def task():
    tasks = Task.query.order_by(case(value=Task.priority, whens={'low':2, 'medium':1, 'high':0}), Task.created).all()
    return render_template('tasks.html', title='Список завдань',tasks=tasks)

@task_bp.route('/category', methods=["GET", "POST"])
def category():
    categories = Category.query.all()
    return render_template('categories.html', title='Список категорій', categories=categories)

@task_bp.route('/employee', methods=["GET", "POST"])
def employee():
    employers = Employee.query.all()
    return render_template('employers.html', title='Список категорій', employers=employers)


@task_bp.route('/task/create', methods=["GET", "POST"])
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
        return redirect(url_for('task_bp_in.task'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('task_bp_in.task_create'))
    return render_template('task_create.html', form=form, title='Task create')

@task_bp.route('/category/create', methods=["GET", "POST"])
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
        return redirect(url_for('task_bp_in.task'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('task_bp_in.category_create'))
    return render_template('category_create.html', form=form, title='Category create')

@task_bp.route('/employee/create', methods=["GET", "POST"])
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
        return redirect(url_for('task_bp_in.employee'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('task_bp_in.employee_create'))
    return render_template('employee_create.html', form=form, title='Employee create')

@task_bp.route('/task/<int:id>', methods=["GET", "POST"])
def task_show(id):
    task = Task.query.get_or_404(id)
    # print(task[0][0].employee_backref)
    # print(task[0])
    return render_template('task_show.html', task=task)

@task_bp.route('/category/<int:id>', methods=["GET", "POST"])
def category_show(id):
    category = Category.query.get(id)
    return render_template('category_show.html',category=category)

@task_bp.route('/employee/<int:id>', methods=["GET", "POST"])
def employee_show(id):
    employee = Employee.query.get_or_404(id)
    # tasks = db.session.query(Task).filter(Task.employee_backref.contains(employee)).all()
    tasks = db.session.query(Task).filter(Task.employee_backref.contains(employee))
    print(tasks)
    return render_template('employee_show.html', employee=employee, tasks=tasks)

@task_bp.route('/task/<int:id>/update', methods=["GET", "POST"])
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
        return render_template('task_update.html', title='Task Update', form=form)

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
            return redirect(url_for('task_bp_in.task'))
        else:
            flash('Error when walidate!', 'danger')
            return redirect(f'/task/{id}/update')

@task_bp.route('/category/<int:id>/update', methods=["GET", "POST"])
def category_update(id):
    form = CategoryCreate()
    category = Category.query.get_or_404(id)

    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.name.data = category.name
        return render_template('category_update.html', title='Category Update', form=form)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            category.name = form.name.data
            try:
                db.session.commit()
                flash('Category seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update category!', 'danger')
            return redirect(url_for('task_bp_in.task'))
        else:
            flash('Error when walidate!', 'danger')
            return redirect(f'/category/{id}/update')


@task_bp.route('/employee/<int:id>/update', methods=["GET", "POST"])
def employee_update(id):
    form = EmployeeCreate()
    employee = Employee.query.get_or_404(id)

    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.name.data = employee.name
        return render_template('employee_update.html', title='Employee Update', form=form)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            employee.name = form.name.data
            try:
                db.session.commit()
                flash('Employee seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update employee!', 'danger')
            return redirect(url_for('.employee'))
        else:
            flash('Error when walidate!', 'danger')
            return redirect(f'/employee/{id}/update')


@task_bp.route('/task/<int:id>/delete', methods=["GET", "POST"])
def task_delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task seccessfully deleted', 'success')
    except:
        flash('Error while delete task!', 'danger')
    return redirect(url_for('.task'))

@task_bp.route('/category/<int:id>/delete', methods=["GET", "POST"])
def category_delete(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category seccessfully deleted', 'success')
    except:
        flash('Error while category deleted!', 'danger')
    return redirect(url_for('.task'))

@task_bp.route('/employee/<int:id>/delete', methods=["GET", "POST"])
def employee_delete(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee seccessfully deleted', 'success')
    except:
        flash('Error while employee deleted!', 'danger')
    return redirect(url_for('.employee'))