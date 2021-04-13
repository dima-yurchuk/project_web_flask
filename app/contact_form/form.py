from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


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