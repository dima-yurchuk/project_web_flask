from app.task.models import  Task, MyEnum, Category, Employee
from app import db
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from app.api_restfull import api_restfull_bp
from flask import jsonify, request, make_response
import datetime

api = Api(api_restfull_bp)
resource_fields = {
    'id' : fields.Integer,
    'title' : fields.String,
    'description': fields.String,
    'created' : fields.String,
    'priority' : fields.String,
    'is_done' : fields.Boolean
}

task_create = reqparse.RequestParser()
task_create.add_argument('title', type=str, help='Title is required', required=True)
task_create.add_argument('description', type=str, help='Description is required', required=True)
task_create.add_argument('priority', type=str, help='Priority is required', required=True)
task_create.add_argument('category_id', type=int, help='Category id is required', required=True)

task_update = reqparse.RequestParser()
task_update.add_argument('title', type=str, help='Title is required', required=True)
task_update.add_argument('description', type=str, help='Description is required', required=True)
task_update.add_argument('created', type=str, help='Created is required', required=True)
task_update.add_argument('priority', type=str, help='Priority is required', required=True)
task_update.add_argument('is_done', type=str, help='Is done is required', required=True)
task_update.add_argument('category_id', type=int, help='Category id is required', required=True)

class TaskItem(Resource):

    def post(self):
        args = task_create.parse_args()
        try:
            task = Task(title=args['title'], description=args['description'], priority=args['priority'], category_id=args['category_id'])
            db.session.add(task)
            db.session.commit()
            # return jsonify({'message': 'Data add in db!'}), 201 777   ?????
            return make_response(jsonify({'message': 'Data add in db!'}), 201)
        except:
            db.session.rollback()
            # return jsonify({'message': 'Error when adding data!'}) ?????
            return make_response(jsonify({'message': 'Error when adding data!'}), 201)



    @marshal_with(resource_fields, envelope='resource')
    def get(self, id=None):
        if id is None:
            tasks_all = Task.query.all()
            return tasks_all
        else:
            task = Task.query.filter_by(id=id).first()
            return task

    @marshal_with(resource_fields, envelope='resource')
    def delete(self, id):
        task = Task.query.filter_by(id=id).first()
        if not task:
            return jsonify({'message': 'Task not found!'}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'The task has been deleted'})

    @marshal_with(resource_fields, envelope='resource')
    def put(self, id):
        task = Task.query.filter_by(id=id).first()
        if not task:
            return jsonify({'message': 'Task not found!'}), 404
        args = task_update.parse_args()

        task.title = args['title']
        task.description = args['description']
        task.created = datetime.datetime.strptime(args['created'], '%a, %d %b %Y %H:%M:%S %Z')
        task.priority = args['priority']
        if args['is_done']=='True':
            task.is_done = True
        elif args['is_done']=='False':
            task.is_done = False
        task.category_id = args['category_id']
        db.session.commit()
        return jsonify({"message": "Task succesfully update!"})



# api.add_resource(TaskItem, '/tasks')
api.add_resource(TaskItem, '/tasks', '/tasks/<int:id>')
# api.add_resource(TaskItem, '/tasks/<int:id>')
# api.add_resource(TaskItem, '/tasks')