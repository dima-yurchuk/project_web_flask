from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, TextAreaField, \
    BooleanField, SelectField, IntegerField, SelectMultipleField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, \
    ValidationError, Regexp
from datetime import datetime
from .models import Task, Category, Employee, User
from . import db

class ContactForm(FlaskForm):
    name = StringField(
            'Name',
            validators=[DataRequired(message="Поле не можу бути пустим!")],
            render_kw={'size':31}
        )
    email = StringField(
            'Email',
            validators=[
                DataRequired(),
                Email(message='Incorrect email address!')
            ],
            render_kw={'size': 31}
        )
    body = TextAreaField(
            'Body',
            validators=[
                DataRequired(),
                Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")
            ],
            render_kw={'cols':35, 'rows': 5}
        )
    submit = SubmitField('Submit')


# def getAgencyList():
#     return [(elem.id, elem.name) for elem in Category.query.all()]


class FormTaskCreate(FlaskForm):
    # def __init__(self, category, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.category=category
    #
    title = StringField(
            'Title',
            validators=[DataRequired(message="Поле не можу бути пустим!")],
            render_kw={'size':31}
        )
    description = TextAreaField(
            'Description',
            validators=[
                DataRequired(),
                Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")
            ],
            render_kw={'cols':35, 'rows': 5}
        )
    priority = SelectField(
        'Priority',
        choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')]
    )
    category = SelectField(
        'Category',
        coerce=int
    )
    employee = SelectMultipleField(
        'Employers',
        coerce=int
    )
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the agency field
        form.category.choices = [(elem.id, elem.name) for elem in Category.query.all()]
        form.employee.choices = [(elem.id, elem.name) for elem in Employee.query.all()]
        return form
    submit = SubmitField('Submit')

class FormTaskUpdate(FlaskForm):
    title = StringField(
            'Title',
            validators=[DataRequired(message="Поле не можу бути пустим!")],
            render_kw={'size':31}
        )
    description = TextAreaField(
            'Description',
            validators=[
                DataRequired(),
                Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")
            ],
            render_kw={'cols':35, 'rows': 5}
        )
    created = DateField(
        'Created'
        # default=datetime.today()
         # format='%Y-%m-%d'
    )
    priority = SelectField(
        'Priority',
        choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')]
    )
    is_done = BooleanField(
        'is_done'
    )
    category = SelectField(
        'Category',
        coerce=int
    )
    employee = SelectMultipleField(
        'Employers',
        coerce=int
    )
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the agency field
        form.category.choices = [(elem.id, elem.name) for elem in Category.query.all()]
        form.employee.choices = [(elem.id, elem.name) for elem in Employee.query.all()]
        return form
    submit = SubmitField('Submit')

class CategoryCreate(FlaskForm):
    name = StringField(
            'Name',
            validators=[DataRequired(message="Поле не можу бути пустим!")],
            render_kw={'size':31}
        )
    submit = SubmitField('Submit')

class EmployeeCreate(FlaskForm):
    name = StringField(
            'Name',
            validators=[DataRequired(message="Поле не можу бути пустим!")],
            render_kw={'size':31}
        )
    count_of_completed_tasks = IntegerField(
        'Count of completed tasks'
    )
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[Length(min=3, max=30,message='Поле повинно бути довжиною від 3 до 30 симолів!'),
        DataRequired(message="Це поле є обов'язковим!"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               "Ім'я повинно містити тільки англійські літери, цифри, крапку або нижнє підкреслення!")
        ]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(message='Некоректна email адреса!')]
    )
    password = PasswordField(
        'Password',
        validators=[Length(min=8,
        message='Поле повинно бути довжиною більше 8 символів!'),
                    DataRequired(message="Це поле є обов'язковим!")]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password', message='Паролі не збігаються!')]
    )
    submit = SubmitField('Sing up')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email уже існує!')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Користувач з таким ім'я вже існує!")


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(),  Email(message='Некоректна email адреса!')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Це поле є обов'язковим!")]
    )
    remember =  BooleanField('Remember me')
    submit = SubmitField('Login')