from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, validators, RadioField, HiddenField, IntegerField, SelectField, MultipleFileField
from wtforms.fields.html5 import TelField
from flask_wtf.file import FileField, FileAllowed, FileRequired

phone_number_regexp = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=100)])
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=3, max=50)])
    address = StringField('Adress', [validators.DataRequired()])
    phone_number = TelField('Phone Number', [validators.DataRequired(),
                                             validators.Regexp(phone_number_regexp, message='Invalid Phone Number')])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])
class AdminAddForm(RegisterForm):
    is_admin = RadioField('Role', choices=[('0', 'User'), ('1', 'Admin')], default=0)

class AdminEditForm(RegisterForm):
    user_id = HiddenField()
    is_admin = RadioField('Role', choices=[('0','User'),('1','Admin')], default=0)
    password = PasswordField('Password', [
        validators.Optional(),
        validators.DataRequired(),
        validators.Length(min=6, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [validators.Optional(), validators.DataRequired()])
    edit_password = BooleanField('Edit Password', default=False)

class EditProfileForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=3, max=50)])
    address = StringField('Adress', [validators.DataRequired()])
    phone_number = TelField('Phone Number', [validators.DataRequired(),
                                             validators.Regexp(phone_number_regexp, message='Invalid Phone Number')])

class ChangePassword(FlaskForm):
    old_password = PasswordField('Password', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


class AddPlantForm(FlaskForm):
    name = StringField('Plant Name', [validators.DataRequired(),validators.Length(min=2, max=100)])
    avatar = FileField('Plant Avatar', [validators.Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class EditPlantForm(AddPlantForm):
    plant_id = HiddenField()

class AddPhaseForm(FlaskForm):
    plant_id = HiddenField(id="add-phase-plant_id")
    name = StringField('Phase Name', [validators.DataRequired(),validators.Length(min=2, max=100)])
    order = IntegerField('Order of Phase', [validators.DataRequired()])
    number_of_days = IntegerField('Number of Days', [validators.DataRequired()])

class EditPhaseForm(FlaskForm):
    phase_id = HiddenField(id="edit-phase-id")
    name = StringField('Phase Name', [validators.DataRequired(), validators.Length(min=2, max=100)])
    order = IntegerField('Order of Phase', [validators.DataRequired()])
    number_of_days = IntegerField('Number of Days', [validators.DataRequired()])

class UploadImageForm(FlaskForm):
    user_id = HiddenField()
    image = FileField('Plant Image', [FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    phase_id = SelectField('Phase', coerce=int, validators=[validators.DataRequired()])

class AddFeatureForm(FlaskForm):
    name = StringField('Feature Name', [validators.DataRequired(),validators.Length(min=2, max=100)])

class AddPhaseFeatureForm(FlaskForm):
    feature_id = SelectField('Feature', coerce=int, validators=[validators.DataRequired()])

class UploadZipForm(FlaskForm):
    zip_file = FileField('Plant Images 30 Days', [FileRequired(), FileAllowed(['zip'], 'Zip only!')])
    phase_id = SelectField('Phase', coerce=int, validators=[validators.DataRequired()])