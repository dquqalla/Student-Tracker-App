# Import FlaskWTF
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators

# Validate login form
class loginForm(FlaskForm):
    username = StringField('username', validators = [validators.DataRequired()])
    password = PasswordField('password', validators =[validators.DataRequired()])
    submit = SubmitField('Login', [validators.DataRequired()])

# Validate register form
class registerForm(FlaskForm):
    username = StringField('username', validators = [validators.DataRequired()])
    password = PasswordField('password', validators =[validators.DataRequired(), validators.Length(min=6)])
    password2 = PasswordField('password2', validators=[validators.DataRequired(),
        validators.EqualTo('password', message='Sorry, passwords do not match.')])
    submit = SubmitField('Sign-up', [validators.DataRequired()])



