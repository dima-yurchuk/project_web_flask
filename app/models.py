from . import db
import enum
from datetime import datetime

class MyEnum(enum.Enum):
    low = 1
    medium = 2
    high = 3

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created = db.Column(db.Date,default=datetime.utcnow())
    priority = db.Column(db.Enum(MyEnum), default='low')
    is_done = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Task {self.id} {self.title} {self.description} {self.created} {self.priority} {self.is_done}>'
