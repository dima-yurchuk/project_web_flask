from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, TextAreaField, \
    BooleanField, SelectField, IntegerField, SelectMultipleField, PasswordField, \
    DateTimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, \
    ValidationError, Regexp


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



# class ChangePassword(FlaskForm):
#     old_password = PasswordField(
#         'Old password',
#         validators=[DataRequired(message="Це поле є обов'язковим!")]
#     )
#     password = PasswordField(
#         'Password',
#         validators=[Length(min=8,
#         message='Поле повинно бути довжиною більше 8 символів!'),
#                     DataRequired(message="Це поле є обов'язковим!")]
#     )
#     confirm_password = PasswordField(
#         'Confirm password',
#         validators=[DataRequired(), EqualTo('password', message='Паролі не збігаються!')]
#     )
#     submit = SubmitField('Change')