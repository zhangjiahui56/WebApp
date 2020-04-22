from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, validators, RadioField, HiddenField

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=100)])
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=3, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

class AdminEditForm(RegisterForm):
    user_id = HiddenField()
    is_admin = RadioField('Role', choices=[('0','User'),('1','Admin')], default=0)
