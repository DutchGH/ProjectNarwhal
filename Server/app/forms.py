from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, validators, BooleanField, DateTimeField
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

class CreateClass(Form):
    course = IntegerField( 'course', validators= [InputRequired()] )
    title = StringField( 'title', validators = [InputRequired()] )
    description = StringField( 'description', validators = [InputRequired()] )
    capacity = IntegerField( 'capacity', validators= [InputRequired()] )
    startTime = DateTimeField( 'startTime', validators = [InputRequired()] )
    duration = IntegerField( 'duration', validators= [InputRequired()] )
    trainer = IntegerField( 'trainer', validators= [InputRequired()] )
    room = IntegerField( 'room', validators= [InputRequired()] )
    reqFac = StringField( 'reqFac', validators = [InputRequired()] )

# class CreateCourse(Form):
#
#
# class AddTrainer(Form):
#
# class AddDelegate(Form):
