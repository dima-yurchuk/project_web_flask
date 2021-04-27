from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .task.models import Task
from datetime import datetime



def tasks(count=30):
    fake = Faker()
    i = 0
    while i < count:
        task = Task(title=fake.text(),
        description=fake.text(),
        priority='low',
        category_id = 1)
        db.session.add(task)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
