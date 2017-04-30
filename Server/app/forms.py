from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, validators, BooleanField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo


class LoginForm(Form):
    username = StringField('username', validators = [InputRequired()])
    password = PasswordField('password', validators = [InputRequired()])

class CreateTrainer(Form):
    name = StringField('name', validators = [InputRequired()])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    address = StringField('address', validators = [InputRequired()])
    phone = IntegerField('phone', validators = [InputRequired()]);
    username = StringField('username', filters = [lambda x: x or None])
    password = PasswordField('password', validators = [EqualTo('confirm', message='Passwords must match')], filters = [lambda x: x or None])
    confirm = PasswordField('confirm', filters = [lambda x: x or None])


class CreateDelegate(Form):
    name = StringField('name', validators = [InputRequired()])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    username = StringField('username', filters = [lambda x: x or None])
    password = PasswordField('password', validators = [EqualTo('confirm', message='Passwords must match')], filters = [lambda x: x or None])
    confirm = PasswordField('confirm', filters = [lambda x: x or None])


class CreateTrainingRoom(Form):
    building = StringField('building', validators = [InputRequired()])
    roomCode = StringField('roomCode', validators = [InputRequired()])
    location = StringField('location', validators = [InputRequired()])
    roomType = SelectField('roomType',
                           choices = [('Seminar Room', 'Seminar Room'), ('Lecture Hall', 'Lecture Hall'), ('Conference Suite', 'Conference Suite')], validators = [InputRequired()])
    capacity = IntegerField('capacity', validators = [InputRequired()])
    # picURL = StringField( 'picURL', validators = [InputRequired()])
    accessRating = SelectMultipleField('accessRating', choices = [('A', 'Assitive Learning System'), ('W', 'Wheelchair Access'), ('L', 'Level Access')])


class CreateClass(Form):
    course = SelectField('course', choices = [], validators = [InputRequired()])
    title = StringField('title', validators = [InputRequired()])
    description = StringField('description', validators = [InputRequired()])
    capacity = IntegerField('capacity', validators = [InputRequired()])
    startTime = DateTimeField('startTime', validators = [InputRequired()])
    duration = SelectField('duration',  choices = [(1, '1 Week'), (2, '2 Week'), (3, '3 Week'), (4, '4 Week'), (5, '5 Week'), (6, '6 Week'), (7, '7 Week'), (8, '8 Week'),
        	                                       (9, '9 Week'), (10, '10 Week'), (11, '11 Week'), (12, '12 Week')], validators = [InputRequired()])
    trainer = SelectField('trainer', choices = [], validators = [InputRequired()])
    room = SelectField('room', choices = [], validators = [InputRequired()])
    reqFac = SelectMultipleField('reqFac', choices = [('M', 'Microphone'), ('D', 'DVD player'), ('P','Projector'), ('I', 'Interactive white board'), ('L', 'Lectern'), ('C', 'Chalkboard'), ('S', 'Computer suite')])
    preReqs = SelectMultipleField('preReqs', choices = [])


class CreateCourse(Form):
    title = StringField('title', validators = [InputRequired()])
    description = StringField('description', validators = [InputRequired()])
