from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, SelectField, IntegerRangeField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Regexp
from blog.models import User
from flask_wtf.file import FileField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^\w{6,12}$', message='Your username should be between 6 and 12 characters long and can only contain letters and numbers.')])
    name = StringField('Name', validators=[DataRequired(), Regexp('^[a-zA-z]{1,}[a-zA-z ]*$', message='Your name can only contain letters, and cannot have any leading spaces.')])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Invalid email address'), EqualTo('confirmEmail', message='Email addresses must match')])
    confirmEmail = EmailField('Confirm Email', validators=[DataRequired(), Email(message='Invalid email address')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Login')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment here!', validators=[DataRequired()])

class RatingForm(FlaskForm):
    rating = IntegerRangeField('Leave a rating here!', validators=[DataRequired()])

class ForgotForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email('Invalid email address')])

class PasswordRecoveryForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm', validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('Old Password', validators=[DataRequired()])
    newPassword = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm', validators=[DataRequired()])

class UpdateDetailsForm(FlaskForm):
    username = StringField('Username', validators=[Regexp('^\w{6,12}$', message='Your username should be between 6 and 12 characters long and can only contain letters and numbers.')])
    name = StringField('Name', validators=[Regexp('^[a-zA-z]{1,}[a-zA-z ]*$', message='Your name can only contain letters, and cannot have any leading spaces.')])

class MFAForm(FlaskForm):
    otp = StringField('OTP')

class VerifyPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])

class ImageUploadForm(FlaskForm):
    pic = FileField('Image Upload')

class ImageDeleteForm(FlaskForm):
    delete_file = SelectField('Remove File', validators=[DataRequired()])