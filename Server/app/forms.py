from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, validators, BooleanField
from wtforms.validators import InputRequired

class LoginForm(Form):
    username = StringField( 'username', validators = [InputRequired()] )
    password = PasswordField( 'password', validators = [InputRequired()] )

class CreateTrainingRoom(Form):
	capacity = IntegerField( 'capacity', validators = [InputRequired()] )
	roomType = StringField( 'roomType', validators = [InputRequired()] )
	picURL = StringField( 'picURL', validators = [InputRequired()] )
	accessRating = StringField( 'accessRating', validators = [InputRequired()] )
	location = StringField( 'location', validators = [InputRequired()] )

# class CreateCourse(Form):
#
#
# class AddTrainer(Form):
#
# class AddDelegate(Form):
