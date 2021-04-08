from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, TextAreaField, \
    BooleanField, SelectField, IntegerField, SelectMultipleField, PasswordField, \
    DateTimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, \
    ValidationError, Regexp
from .models import Task, Category, Employee, User
from flask_wtf.file import FileField, FileAllowed


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

class UpdateAccountForm(FlaskForm):
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
    about_me = TextAreaField(
                'About me',
                validators=[
                    DataRequired(),
                    Length(max=400, message="The field must not contain more than 400 characters!")
                ],
                render_kw={'cols':35, 'rows': 5}
           )
    # last_seen = DateTimeField('Last seen', validators=[DataRequired()])
    picture = FileField('Update prifile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    old_password = PasswordField(
        'Old password',
        validators=[DataRequired(message="Це поле є обов'язковим!")]
    )
    password = PasswordField(
        'Password',
        validators=[Length(min=8,
                           message='Поле повинно бути довжиною більше 8 символів!'),
                    DataRequired(message="Це поле є обов'язковим!")]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(message="Це поле є обов'язковим!"), EqualTo('password', message='Паролі не збігаються!')]
    )
    submit = SubmitField('Update')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() and self.old_password.data and self.password.data and self.confirm_password.data: # якщо ми змінюємо ТІЛЬКИ пароль
            self.email.flags.disabled = False  # вимикаємо перевірку email
        elif User.query.filter_by(email=field.data).first() and not (
                self.old_password.data or self.password.data or self.confirm_password.data) and self.picture.data:
            # якщо ми змінюємо тільки фото
            self.old_password.validators.insert(0, Optional())
            self.password.validators.insert(0, Optional())
            self.confirm_password.validators.insert(0, Optional())
            self.email.flags.disabled = False
            self.username.flags.disabled = False
        elif User.query.filter_by(email=field.data).first() and not(self.old_password.data or self.password.data or self.confirm_password.data):
            # якщо ми змінюємо ТІЛЬКИ ім'я і email і користувач вже існує
            self.old_password.validators.insert(0, Optional())  # вимикаємо перевірку пароля
            self.password.validators.insert(0, Optional())
            self.confirm_password.validators.insert(0, Optional())
            raise ValidationError('Email уже існує!')
        else:#  якщо ми змінюємо ТІЛЬКИ ім'я і email і користувача НЕ існує в БД
            self.old_password.validators.insert(0, Optional())
            self.password.validators.insert(0, Optional())
            self.confirm_password.validators.insert(0, Optional())
                # raise ValidationError('Email уже існує!')
        # elif User.query.filter_by(email=field.data).first():
        #     raise ValidationError('Email уже існує!')
    def validate_username(self, field):
        if User.query.filter_by(
                username=field.data).first() and self.old_password.data and self.password.data and self.confirm_password.data: # якщо ми змінюємо ТІЛЬКИ пароль
            self.username.flags.disabled = False  # вимикаємо перевірку username
        elif User.query.filter_by(username=field.data).first() and not (
                self.old_password.data or self.password.data or self.confirm_password.data) and self.picture.data:
            # якщо ми змінюємо тільки фото
            self.old_password.validators.insert(0, Optional())
            self.password.validators.insert(0, Optional())
            self.confirm_password.validators.insert(0, Optional())
            self.email.flags.disabled = False
            self.username.flags.disabled = False
        elif User.query.filter_by(username=field.data).first() and not (
                self.old_password.data or self.password.data or self.confirm_password.data):
            # якщо ми змінюємо ТІЛЬКИ ім'я і email і користувач вже існує
            self.old_password.validators.insert(0, Optional())
            self.password.validators.insert(0, Optional())
            self.confirm_password.validators.insert(0, Optional())
            raise ValidationError("Користувач з таким ім'я вже існує!")
        else: #  якщо ми змінюємо ТІЛЬКИ ім'я і email і користувача НЕ існує в БД
            self.old_password.validators.insert(0, Optional())
            self.password.validators.insert(0, Optional())
            self.confirm_password.validators.insert(0, Optional())
    def validate_password(self, field):
        if not self.old_password.data or not self.password.data or not self.confirm_password.data:
            raise ValidationError("Для зміни паролю необхідно заповнити 3 поля!")

    def validate_old_password(self, field):
        if not self.old_password.data or not self.password.data or not self.confirm_password.data:
            raise ValidationError("Для зміни паролю необхідно заповнити 3 поля!")

    def validate_confirm_password(self, field):
        if not self.old_password.data or not self.password.data or not self.confirm_password.data:
            raise ValidationError("Для зміни паролю необхідно заповнити 3 поля!")
            # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email уже існує!')
    #
    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError("Користувач з таким ім'я вже існує!")


class ChangePassword(FlaskForm):
    old_password = PasswordField(
        'Old password',
        validators=[DataRequired(message="Це поле є обов'язковим!")]
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
    submit = SubmitField('Change')