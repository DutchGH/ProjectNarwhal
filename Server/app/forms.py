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
    course = SelectField('course', coerce = int, choices = [], validators = [InputRequired()])
    title = StringField('title', validators = [InputRequired()])
    description = StringField('description', validators = [InputRequired()])
    capacity = IntegerField('capacity', validators = [InputRequired()])
    duration = SelectField('duration', coerce = int, choices = [(1, '1 Week'), (2, '2 Weeks'), (3, '3 Weeks'), (4, '4 Weeks'), (5, '5 Weeks'), (6, '6 Weeks'), (7, '7 Weeks'), (8, '8 Weeks'),
        	                                       (9, '9 Weeks'), (10, '10 Weeks'), (11, '11 Weeks'), (12, '12 Weeks')], validators = [InputRequired()])
    trainer = SelectField('trainer', coerce = int, choices = [], validators = [InputRequired()])
    room = SelectField('room', coerce = int, choices = [], validators = [InputRequired()])
    reqFac = SelectMultipleField('reqFac', choices = [('M', 'Microphone'), ('D', 'DVD player'), ('P','Projector'), ('I', 'Interactive white board'), ('L', 'Lectern'), ('C', 'Chalkboard'), ('S', 'Computer suite')])
    preReqs = SelectMultipleField('preReqs', coerce = int, choices = [])

class CreateClassDate(Form):
    dateYear = SelectField('dateYear', coerce = int, choices = [(2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020')], validators = [InputRequired()])
    dateMonth = SelectField('dateMonth',  coerce = int, choices = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                                                     (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], validators = [InputRequired()])
    dateDay = SelectField('dateDay',  coerce = int, choices = [(1, '1'), (2, '2'), ( 3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),
                                                               (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'),
                                                               (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'),
                                                               (31, '31')], validators = [InputRequired()])
    dateHour = SelectField('dateHour', coerce = int, choices = [(9, '09:00'), (10, '10:00'), (11, '11:00'), (12, '12:00'), (13, '13:00'), (14, '14:00'), (15, '15:00'), (16, '16:00'),
                                                                (17, '17:00'), (18, '18:00')], validators = [InputRequired()])

class CreateCourse(Form):
    title = StringField('title', validators = [InputRequired()])
    description = StringField('description', validators = [InputRequired()])
