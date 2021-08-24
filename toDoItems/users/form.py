from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, PasswordField, BooleanField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import EqualTo, Email, Length, InputRequired, ValidationError
from flask_login  import current_user
from toDoItems.models import User




# REGISTRATION FORM
class RegistrationForm(FlaskForm):
    fullname = StringField(label = 'Fullname', validators = [Length(min = 10, max = 80, message = 'name should be atleast 10 characters long'),
                                                             InputRequired()])
    username = StringField(label = 'Username', validators=[InputRequired(), Length(min = 10, max = 100, message = 'username should contain atelast 10 characters')])
    email = StringField(label = 'Email', validators=[InputRequired(), Email(message = 'email address should be valid'), 
                                                    Length(min = 10, max = 80, message = 'email should be atleast 10 characters long')])
    dob = DateField(label = 'Date of birth', validators=[InputRequired()])
    gender = RadioField(label = 'Gender', choices = [('Female', 'Female'), ('Male', 'Male')], validators = [InputRequired()])
    password = PasswordField(label = 'Password', validators=[InputRequired(), Length(min=8, max=100, message='password should be atleast 10 characters long')])
    confirm_password = PasswordField(label = 'Confirm password', validators = [InputRequired(), EqualTo('password', message = 'password should be similar in both columns')])
    recaptcha = RecaptchaField()
    submit = SubmitField(label = 'Register')        

    # CUSTOMIZABLE VALIDATORS
    def validate_fullname(self, fullname):
        invalidKeywords = '!@#$%^&*()_+-={[]:;"}?/><,.~`|\'///'
        totalInvalidChars = 0
        for char in fullname.data:
            if char in invalidKeywords:
                totalInvalidChars += 1
        if totalInvalidChars > 0:
            raise ValidationError('name should not contain any invalid characters')
    
    def validate_password(self, password):
        specialKeywords = '!@#$%^&*()_+-={[]:;"}?/><,.~`|\'///'
        totalSpecialChars = 0
        for char in password.data:
            if char in specialKeywords:
                totalSpecialChars += 1
        if totalSpecialChars == 0:
            raise ValidationError('password should contain atleast one special character')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already taken, try different username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('user with this email address is already registered')



# LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField(label = 'Email', validators=[InputRequired(), Email(message = 'email address should be valid'), 
                                                    Length(min = 10, max = 80, message = 'email should be atleast 10 characters long')])
    password = PasswordField(label = 'Password', validators=[InputRequired(), Length(min=8, max=100, message='password should be atleast 10 characters long')])
    remember = BooleanField(label = 'Remember me')
    submit = SubmitField(label = 'Login')    



# # FORM FOR UPDATING USER DETAILS
class AccountUpdateForm(FlaskForm):
    fullname = StringField(label = 'Fullname', validators = [Length(min = 10, max = 80, message = 'name should be atleast 10 characters long'),
                                                             InputRequired()])
    username = StringField(label = 'Username', validators=[InputRequired(), Length(min = 10, max = 100, message = 'username should contain atelast 10 characters')])
    email = StringField(label = 'Email', validators=[InputRequired(), Email(message = 'email address should be valid'), 
                                                    Length(min = 10, max = 80, message = 'email should be atleast 10 characters long')])
    picture = FileField(label = 'Upload Profile Picture', validators=[FileAllowed(['jpg','jpeg','png','gif','svg'], 
                                                                    message = 'file in gif, jpeg, jpg, png & svg formats are only allowed.')])
    submit = SubmitField(label = 'Update')        

    # CUSTOMIZABLE VALIDATORS
    def validate_fullname(self, fullname):
        if current_user.fullname != fullname.data:
            invalidKeywords = '!@#$%^&*()_+-={[]:;"}?/><,.~`|\'///'
            totalInvalidChars = 0
            for char in fullname.data:
                if char in invalidKeywords:
                    totalInvalidChars += 1
            if totalInvalidChars > 0:
                raise ValidationError('name should not contain any invalid characters')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username is already taken, try different username')
    
    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('user with this email address is already registered')



# REQUESTING FORM FOR RESETTING PASSWORD
class RequestResetForm(FlaskForm):
    email = StringField(label = 'Email', validators=[InputRequired(), Email(message = 'email address should be valid'), Length(min = 10, max = 80, message = 'email should be atleast 10 characters long')])
    submit = SubmitField(label = 'Request Password Reset')



# RESETTING PASSWORD FORM
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label = 'Password', validators=[InputRequired(), Length(min=8, max=100, message='password should be atleast 10 characters long')])
    confirm_password = PasswordField(label = 'Confirm password', validators = [InputRequired(), EqualTo('password', message = 'password should be similar in both columns')])
    submit = SubmitField(label = 'Reset Password') 

    def validate_password(self, password):
        specialKeywords = '!@#$%^&*()_+-={[]:;"}?/><,.~`|\'///'
        totalSpecialChars = 0
        for char in password.data:
            if char in specialKeywords:
                totalSpecialChars += 1
        if totalSpecialChars == 0:
            raise ValidationError('password should contain atleast one special character')