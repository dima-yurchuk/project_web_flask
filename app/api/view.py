from flask import render_template, request, redirect, url_for, flash, jsonify, make_response


from app.task import task_bp
from app.task.models import  Task, Category, Employee
from app import db
from sqlalchemy import case
from flask_login import login_user, current_user, logout_user, login_required

from app.api import api_bp
from ..profile.models import User
from app import bcrypt
import jwt
import datetime
from flask import current_app as app
from functools import wraps
from os import abort


def token_required(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      token = None
      if 'x-access-token' in request.headers:
         token = request.headers['x-access-token']
      if not token:
          return jsonify({'message':'Token is missing!'}), 401
      try:
          data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
          current_user = User.query.filter_by(id=data['id']).first()
      except:
          return jsonify({'message':'Token is invalid!'}), 401
      return f(current_user, *args, **kwargs)
   return decorated


@api_bp.route('/login')
def login_api():
   auth=request.authorization
   if not auth or not auth.username or not auth.password:
      return make_response('Could not verify', 401, {'WWW-Authenticated':'Basic realm="Login reguired!"'})

   user = User.query.filter_by(email=auth.username).first()

   if not user:
      return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

   if bcrypt.check_password_hash(user.password, auth.password):
      token = jwt.encode({'id':user.id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

      return jsonify({'token':token})
   return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

@api_bp.route('/tasks', methods=["POST"])
@token_required
def task_create(current_user):
   if not current_user.admin:
      return jsonify({'message':'Cannot perform that function!'})
   data = request.get_json()
   try:
      title = data['title']
      description = data['description']
      # created = form.created.data
      priority = data['priority']
      category_id = data['category_id']

      category_id = db.session.query(Category.id).filter(Category.id == category_id)

      employers = data['employee']

      task = Task(title=title, description=description, priority=priority, category_id=category_id)


      for employee in employers:
         task.employee_backref.append(Employee.query.get_or_404(employee))
      db.session.add(task)
      db.session.commit()
      return jsonify({'message':'Data add in db!'})
   except:
      db.session.rollback()
      flash('Error adding data in DB!', 'danger')
      return jsonify({'message':'Error when adding data!'})


@api_bp.route('/tasks/<int:id>', methods=["DELETE"])
@token_required
def task_delete(current_user,id):
   # if current_user.admin:
   #    return jsonify({'message':'Cannot perform that function!'})
   task = Task.query.filter_by(id=id).first()
   if not task:
       return jsonify({'message': 'Task not found!'})
   db.session.delete(task)
   db.session.commit()
   return jsonify({'message': 'The task has been deleted'})


@api_bp.route('/tasks/<int:id>')
@token_required
def task_show(current_user, id):
   task = Task.query.filter_by(id=id).first()
   if not task:
       return jsonify({'message': 'Task not found!'})
   tasks = []
   task_json = {}
   task_json['id'] = task.id
   task_json['title'] = task.title
   task_json['description'] = task.description
   task_json['created'] = task.created
   task_json['priority'] = str(task.priority.name)
   task_json['is_done'] = task.is_done
   employers = ""
   for empl in task.employee_backref:
      employers = employers + empl.name + " "
   employers.strip()
   task_json['employers'] = employers
   tasks.append(task_json)
   return jsonify({"task":tasks})




@api_bp.route('/tasks')
@token_required
def tasks_show(current_user):
   tasks_all = Task.query.all()
   tasks = []
   for task in tasks_all:
      task_json = {}
      task_json['id'] = task.id
      task_json['title'] = task.title
      task_json['description'] = task.description
      task_json['created'] = task.created
      task_json['priority'] = str(task.priority.name)
      task_json['is_done'] = task.is_done
      employers = ""
      for empl in task.employee_backref:
         employers = employers + empl.name + " "
      employers.strip()
      task_json['employers'] = employers
      tasks.append(task_json)
   return jsonify({"task": tasks})

@api_bp.route('/tasks/<int:id>', methods=["PUT"])
@token_required
def task_update(current_user, id):
   # if current_user.admin:
   #    return jsonify({'message':'Cannot perform that function!'})
   task = Task.query.filter_by(id=id).first()
   if not task:
      return jsonify({'message': 'Task not found!'})

   title = request.json['title']
   description = request.json['description']
   priority = request.json['priority']
   category_id = request.json['category_id']

   task.title = title
   task.description = description
   task.priority = priority
   task.category_id = category_id
   db.session.commit()
   return jsonify({"message":"Task succesfully update!"})
