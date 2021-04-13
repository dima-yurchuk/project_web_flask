from app import db
import enum
from datetime import datetime

class MyEnum(enum.Enum):
    low = 1
    medium = 2
    high = 3

association_table = db.Table('task_empl',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created = db.Column(db.Date,default=datetime.utcnow())
    priority = db.Column(db.Enum(MyEnum), default='low')
    is_done = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return f'<Task {self.id} {self.title} {self.description} {self.created} {self.priority} {self.is_done} {self.category_id}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    category = db.relationship('Task', backref='category_backref', lazy=True)
    def __repr__(self):
        return f'<Task {self.id} {self.name} >'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    count_of_completed_tasks = db.Column(db.Integer)

    task_empl = db.relationship('Task', secondary=association_table, backref=db.backref('employee_backref'))
    def __repr__(self):
        return f'<Task {self.id} {self.name} {self.count_of_completed_tasks}>'