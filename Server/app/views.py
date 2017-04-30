from flask import render_template, session, redirect, flash, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, models, login_manager
from .forms import *
from queries import *
import datetime as dt
import sys
import logging

# This callback is used to reload the user object from the user ID stored
# in the session.


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(id)


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

# The route used to pass a user accID to the view page


@app.route('/')
def home():
    user = current_user
    if user is not None and user.is_authenticated:
        return render_template('index.html', title="FDM TEST", user=user)
    else:
        return render_template('index.html', title="FDM TEST")


@app.route('/timetabletemp')
def timetabletemp():
    return render_template('timetable.html', title="FDM TEST")


# The login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(
            username=request.form['username']).first()
        if user is not None and (user.password == request.form['password']):
            login_user(user)
            flash('Logged in succesfully')
            return redirect('/')
        else:
            flash('Invalid Credentials. Please Try Again')
    return render_template('login.html', title='Log In', form=form)


# logging the user out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# Once user is logged page is displayed <---example--->


@app.route('/adminoptions')
@login_required
def admin():
    if current_user.type != 'Admin':
        abort(403)
    else:
        return render_template('loggedIn.html', title='Home Page')

##

@app.route('/myaccount')
@login_required
def myAccount():
    if current_user.type != 'Delegate':
        abort(403)
    else:
        delClassList = current_user.classList
        return render_template('myAccount.html', title='Timetable', delClassList = delClassList)

@app.route('/timetable')
@login_required
def timetable():
    if current_user.type != 'Delegate':
        abort(403)
    classList = current_user.classList
    return render_template('timetable.html', title='Timetable', classList=classList)

# Displays a list of trainers which can link to the trainers schedule.


@app.route('/trainers')
@login_required
def trainerList():
    if current_user.type != 'Admin':
        abort(403)
    trainerList = trainers()
    return render_template('trainers.html', title='Trainer List', trainerList=trainerList)

# accessed using <a href='/trainers/{{item.userID}}'></a>



@app.route('/courses')
@login_required
def courseList():
    if current_user.type != 'Admin':
        abort(403)
    courseList = courses()
    return render_template('courses.html', title='Trainer List', courseList = courseList)


@app.route('/course/<id>')
@login_required
def course(id):
    courseID = id
    if current_user.type != 'Admin':
        abort(403)

    current_course = courses(courseID = courseID)
    #courseClassList = classes(courseID = current_course.courseID)
    courseClassList = classes(course = current_course)
    #courseClassList = models.Class.query.filter_by(courseID = current_course.courseID)
    if type(courseClassList) != list:
        courseClassList = [courseClassList]

    return render_template('courseDetails.html', title='Trainer Schedule',current_course = current_course, courseClassList = courseClassList)


@app.route('/class/<id>')
@login_required
def adminClassDetails(id):
    classID = id
    if current_user.type != 'Admin':
        abort(403)
    current_class = classes(classID = classID)
    return render_template('adminClassDetails.html', title = current_class.title + 'Details', current_class = current_class)
    
##accessed using <a href='/trainers/{{item.userID}}'></a>

@app.route('/trainers/<id>')
@login_required
def trainerSchedule(id):
    trainerID = id
    if current_user.type != 'Admin':
        abort(403)

    current_trainer = trainers(trainerID=trainerID)
    trainerClassList = classes(trainerPoint=trainerID)
    if type(trainerClassList) != list:
        trainerClassList = [trainerClassList]

    return render_template('trainersSched.html', title='Trainer Schedule', current_trainer=current_trainer, trainerClassList=trainerClassList)

##


@app.route('/rooms')
@login_required
def roomList():
    if current_user.type != 'Admin':
        abort(403)
    roomList = rooms()
    return render_template('rooms.html', title='Room List', roomList=roomList)

##


@app.route('/rooms/<id>')
@login_required
def roomSchedule(id):
    roomID = id
    if current_user.type != 'Admin':
        abort(403)
    room = rooms(roomID=id)
    roomClassList = classes(locationPoint=roomID)
    if type(roomClassList) != list:
        roomClassList = [roomClassList]

    return render_template('roomsSched.html', title='Room Schedule', room=room, roomClassList=roomClassList)


@app.route('/addroom', methods=['GET', 'POST'])
@login_required
def addRoom():
    if current_user.type != 'Admin':
        abort(403)
    form = CreateTrainingRoom()
    if form.validate_on_submit():
        ar = ''.join(form.accessRating.data)
        addNewRoom(form.capacity.data, form.roomType.data, ar,
                   form.roomCode.data, form.building.data, form.location.data)
        flash("CREATED SUCCESSFULY")
    return render_template('newRoom.html', title='Add Room', form=form)


@app.route('/addtrainer', methods=['GET', 'POST'])
@login_required
def addTrainer():
    if current_user.type != 'Admin':
        abort(403)
    form = CreateTrainer()
    if form.validate_on_submit():
        if form.username.data is not None:
            username = form.username.data
        else:
            username = form.email.data
        if form.password.data is not None:
            password = form.password.data
        else:
            password = "pass"            
        addNewTrainer(form.name.data, form.address.data, form.phone.data, form.email.data, username, password)
        flash("CREATED SUCCESSFULY")
    return render_template('newTrainer.html', title='Add Trainer', form=form)


@app.route('/createaccount', methods=['GET', 'POST'])
def addDelegate():
    form = CreateDelegate()
    if form.validate_on_submit():
        if form.username.data is not None:
            username = form.username.data
        else:
            username = form.email.data
        if form.password.data is not None:
            password = form.password.data
        else:
            password = "pass"
        addNewDel(form.name.data, username, password, [], form.email.data)
        flash("CREATED SUCCESSFULY")
    return render_template('newDelegate.html', title='Create Account', form=form)



##
@app.route('/delegates')
@login_required
def delList():
    if current_user.type != 'Admin':
        abort(403)
    delList = delegates()
    return render_template('delegates.html', title='Delegate List', delList=delList)

##


@app.route('/delegates/<id>')
@login_required
def delSchedule(id):
    delid = id
    if current_user.type != 'Admin':
        abort(403)

    user = delegates(delID=delid)
    delClassList = user.classList

    return render_template('delsSched.html', title='Delegate Schedule', user=user, delClassList=delClassList)

@app.route('/signup/<id>')
@login_required
def signUp(id):
    classID = id
    thisClass = classes(classID = id)
    if current_user.type == 'Delegate':
        if meetsRequirments(thisClass, current_user):
            addToClass(thisClass, current_user)
            flash("You have been added.")
    else:
        flash("You are not authorised to do this")
    return redirect('/browse/classes/class/' + classID)

@app.route('/browse/classes/class/<id>')
def viewClassDetails(id):
    classID = id
    current_class = classes(classID = classID)
    classSize = classAttendenceLen(current_class)
    if current_user.type == 'Delegate':
        userQualify = meetsRequirements(current_user, current_class)
    else:
        userQualify = False
    return render_template('viewClass.html', title = "Course", current_class = current_class, classSize = classSize, userQualify = userQualify)


