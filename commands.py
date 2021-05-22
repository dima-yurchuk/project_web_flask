import click
from flask.cli import with_appcontext
from app import db
from flask import current_app
from app.profile.models import User
from app.task.models import Task, Category, Employee

@current_app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')

@click.group()
def cli():
    pass


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    click.echo("tables created!!!")
    #print("create_all was maked")


@click.command(name='create_admin')
@with_appcontext
def create_admin():
    click.echo('Hello! Run command ok before')
    nickname = "superadmin"
    admin = True
    u = User(nickname=nickname, admin=admin)
    #print("superadmin created", u)
    db.session.add(u)
    db.session.commit()
    click.echo("superadmin created!!!")

cli.add_command(create_tables)
cli.add_command(create_admin)


if __name__ == '__main__':
    cli()