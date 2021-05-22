import click
from flask.cli import with_appcontext
from app import db
from app.profile.models import User
from app.task.models import Task, Category, Employee

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()