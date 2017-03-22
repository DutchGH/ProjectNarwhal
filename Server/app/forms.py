from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, validators, BooleanField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])


class CreateTrainingRoom(Form):
    building = StringField('building', validators=[InputRequired()])
    roomCode = StringField('roomCode', validators=[InputRequired()])
    location = StringField('location', validators=[InputRequired()])
    roomType = SelectField('roomType',
                           choices=[('Seminar Room', 'Seminar Room'), ('Lecture Hall', 'Lecture Hall'), ('Conference Suite', 'Conference Suite')], validators=[InputRequired()])
    capacity = IntegerField('capacity', validators=[InputRequired()])
    # picURL = StringField( 'picURL', validators = [InputRequired()])
    accessRating = SelectMultipleField('accessRating', choices=[('A', 'All'), ('W', 'Wheelchair Access')])


class CreateClass(Form):
    course=IntegerField('course', validators=[InputRequired()])
    title=StringField('title', validators=[InputRequired()])
    description=StringField('description', validators=[InputRequired()])
    capacity=IntegerField('capacity', validators=[InputRequired()])
    startTime=DateTimeField('startTime', validators=[InputRequired()])
    duration=IntegerField('duration', validators=[InputRequired()])
    trainer=IntegerField('trainer', validators=[InputRequired()])
    room=IntegerField('room', validators=[InputRequired()])
    reqFac=StringField('reqFac', validators=[InputRequired()])



class CreateCourse(Form):
    title=StringField('title', validators=[InputRequired()])
    description=StringField('description', validators=[InputRequired()])

# class AddTrainer(Form):
#
# class AddDelegate(Form):
