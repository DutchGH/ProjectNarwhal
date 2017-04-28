from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, validators, BooleanField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class CreateTrainer(Form):
    name = StringField('name', validators = [InputRequired()])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    address = StringField('address', validators = [InputRequired()])
    phone = IntegerField('phone', validators = [InputRequired()]);
    username = StringField('username')
    password = PasswordField('password')
    confirm = PasswordField('confirm')

class CreateDelegate(Form):
    name = StringField('name', validators = [InputRequired()])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    username = StringField('username', filters = [lambda x: x or None])
    password = PasswordField('password', validators =[EqualTo('confirm', message='Passwords must match')], filters = [lambda x: x or None])
    confirm = PasswordField('confirm', filters = [lambda x: x or None])

class CreateTrainingRoom(Form):
    building = StringField('building', validators=[InputRequired()])
    roomCode = StringField('roomCode', validators=[InputRequired()])
    location = StringField('location', validators=[InputRequired()])
    roomType = SelectField('roomType',
                           choices=[('Seminar Room', 'Seminar Room'), ('Lecture Hall', 'Lecture Hall'), ('Conference Suite', 'Conference Suite')], validators=[InputRequired()])
    capacity = IntegerField('capacity', validators=[InputRequired()])
    # picURL = StringField( 'picURL', validators = [InputRequired()])
    accessRating = SelectMultipleField('accessRating', choices=[('A', 'Assitive Learning System'), ('W', 'Wheelchair Access'), ('L', 'Level Access')])


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
