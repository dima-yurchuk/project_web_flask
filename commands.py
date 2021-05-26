import click
from flask.cli import with_appcontext
from app import db
from app.profile.models import User
from app.task.models import Task, Category, Employee

@click.group()
def cli():
    pass

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
    click.echo("tables created!!!")

cli.add_command(create_tables)


if __name__ == '__main__':
    cli()
# @click.command(name="create_user")
# @with_appcontext
# def create_user():
#     user = User(username='username', email='email', password='password')
#     db.session.add(user)
#     db.session.commit()
