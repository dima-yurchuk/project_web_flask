from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, TextAreaField, \
    BooleanField, SelectField, IntegerField, SelectMultipleField, PasswordField, \
    DateTimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

from .models import Task, Category, Employee


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