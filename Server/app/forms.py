from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, validators, BooleanField
from wtforms.validators import InputRequired

class LoginForm(Form):
    username = StringField( 'username', validators = [InputRequired()] )
    password = PasswordField( 'password', validators = [InputRequired()] )
