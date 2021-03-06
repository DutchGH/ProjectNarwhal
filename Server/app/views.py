from flask import render_template, session, redirect, flash, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required, AnonymousUserMixin
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

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.type = 'Guest'

# If a 403 error code is raised, show the 403 page given by 403.html.
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

# When a user attempts to login, check their username and password.
# If the credentials are valid, login.
# Otherwise, redirect to the homepage and inform the user that the login failed.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(
            username=request.form['username']).first()
        if user is not None and (user.password == request.form['password']):
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid Credentials. Please Try Again')
    return render_template('login.html', title='Log In', form=form)

# Logout the current user and redirect to the homepage.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# When a user tries to access admin options, check their type.
# If they are eligble (i.e. they are an admin), render the page.
# Otherwise, abort with error code 403.
@app.route('/adminoptions')
@login_required
def admin():
    if current_user.type != 'Admin':
        # User does not have correct permissions.
        abort(403)
    else:
        return render_template('loggedIn.html', title='Home Page')

# The user wishes to browse available classes.
# Retreive lists of classes, courses, durations and locations.
# Pass these to the template for rendering.
@app.route('/browse/classes')
def browseClasses():
    classList = browseItems()
    courseList = browseCourses()
    durations = getDurations()
    locations = getLocations()
    return render_template('browseClasses.html', title='Browse Clases', classList=classList, courseList=courseList, durations=durations, locations=locations)

# The user wishes to go to their account page.
# This page depends on whether the user is a trainer, admin, or delegate.
@app.route('/myaccount')
@login_required
def myAccount():
    if current_user.type == 'Delegate':
        delClassList = getClasses(current_user)
        pastClass = history(current_user)
        futureClass = schedule(current_user)
        return render_template('myAccount.html', title='Account Details', pastClass=pastClass, futureClass=futureClass)
    elif current_user.type == 'Trainer':
        teachingList = classes(trainerPoint = current_user.trainerID)
        return render_template('myAccount.html', title='Account Details', teachingList = teachingList)
    else:
        abort(403)

# Render the page that displays a user's timetable.
# This route is only valid for delegates, therefore abort with 403 for any other user type.
@app.route('/timetable')
@login_required
def timetable():
    if current_user.type == 'Delegate':
        classList = delTimeTable(current_user)
        return render_template('timetable.html', title='Timetable', classList=classList)
    if current_user.type == 'Trainer':
        classList = trainerTimeTable(current_user)
        return render_template('trainerTable.html', title='Timetable', classList=classList)
    else:
        abort(403)

# Display a list of trainers.
# Only valid for admins.
@app.route('/trainers')
@login_required
def trainerList():
    if current_user.type != 'Admin':
        abort(403)
    trainerList = trainers()
    return render_template('trainers.html', title='Trainer List', trainerList=trainerList)

# View a list of courses.
# Only valid for admins.
@app.route('/courses')
@login_required
def courseList():
    if current_user.type != 'Admin':
        abort(403)
    courseList = courses()
    return render_template('courses.html', title='Trainer List', courseList=courseList)

# View a list of classes for a given course.
# Only valid for admins.
@app.route('/course/<id>')
@login_required
def course(id):
    courseID = id
    if current_user.type != 'Admin':
        abort(403)

    current_course = courses(courseID=courseID)
    courseClassList = classes(course=current_course)
    if type(courseClassList) != list:
        courseClassList = [courseClassList]

    return render_template('courseDetails.html', title='Trainer Schedule', current_course=current_course, courseClassList=courseClassList)

# View details about a particular class.
# Only valid for admins.
@app.route('/class/<id>')
@login_required
def adminClassDetails(id):
    classID = id
    if current_user.type != 'Admin':
        abort(403)
    current_class = classes(classID=classID)
    attSize = len(current_class.attendanceList)
    return render_template('adminClassDetails.html', title=current_class.title + 'Details', current_class=current_class, attSize = attSize)

# View the schedule for a particular trainer.
# Only valid for admins.
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

@app.route('/rooms')
@login_required
def roomList():
    if current_user.type != 'Admin':
        abort(403)
    roomList = rooms()
    return render_template('rooms.html', title='Room List', roomList=roomList)

@app.route('/rooms/<id>')
@login_required
def roomSchedule(id):
    roomID = id
    if current_user.type != 'Admin':
        abort(403)
    room = rooms(roomID=id)
    fac = checkFacilities(room.facilities)
    ac = checkAccess(room.accessRating)
    roomClassList = classes(locationPoint=roomID)
    tt = roomTimeTable(room)
    if type(roomClassList) != list:
        roomClassList = [roomClassList]

    return render_template('roomsSched.html', title='Room Schedule', room=room, roomClassList=roomClassList, fac = fac, ac = ac, tt = tt)

@app.route('/addroom', methods=['GET', 'POST'])
@login_required
def addRoom():
    if current_user.type != 'Admin':
        abort(403)
    form = CreateTrainingRoom()
    if form.validate_on_submit():
        ar = ''.join(form.accessRating.data)
        fac = ''.join(form.facilities.data)
        addNewRoom(form.capacity.data, form.roomType.data, ar,
                   form.roomCode.data, fac, form.building.data, form.location.data, "http://www.leeds.ac.uk/mtc/images/rooms/mlt.jpg")
        flash("CREATED SUCCESSFULY")
    return render_template('newRoom.html', title='Add Room', form=form)

@app.route('/addtrainer', methods=['GET', 'POST'])
@login_required
def addTrainer():
    if current_user.type != 'Admin':
        abort(403)
    form = CreateTrainer()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if checkUserName(username):
            addNewTrainer(form.name.data, form.address.data,
                          form.phone.data, form.email.data, username, password)
            flash("CREATED SUCCESSFULY")
        else:
            flash("That username is already taken.")
    return render_template('newTrainer.html', title='Add Trainer', form=form)

@app.route('/createaccount', methods=['GET', 'POST'])
def addDelegate():
    form = CreateDelegate()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if checkUserName(username):
            addNewDel(form.name.data, username, password, [], form.email.data)
            flash("CREATED SUCCESSFULY")
        else:
            flash("That username is already taken.")
    return render_template('newDelegate.html', title='Create Account', form=form)

@app.route('/editdel', methods=['GET', 'POST'])
@login_required
def editDelegate():
    if current_user.type != "Delegate":
        abort(403)
    form = EditDelegate()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.oldPassword.data == current_user.password:
                edit(current_user, username=form.username.data,
                     password=form.password.data, email=form.email.data)
                return redirect('/myaccount')
            else:
                flash("Old password was incorrect.")
        else:
            flash("Confirm password did not match.")
    return render_template('editDel.html', title='Edit Account', form=form)

@app.route('/edittrain', methods=['GET', 'POST'])
@login_required
def editTrainer():
    form = EditTrainer()
    if current_user.type != "Trainer":
        abort(403)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.oldPassword.data == current_user.password:
                edit(current_user, username=form.username.data, password=form.password.data,
                     email=form.email.data, phone=form.phone.data, address=form.address.data)
                return redirect('/myaccount')
            else:
                flash("Old password was incorrect.")
        else:
            flash("Confirm password did not match.")
    return render_template('editTrain.html', title='Edit Account', form=form)


@app.route('/addcourse', methods=['GET', 'POST'])
@login_required
def addCourse():
    if current_user.type != 'Admin':
        abort(403)
    form = CreateCourse()
    if form.validate_on_submit():
        addNewCourse(form.title.data, form.description.data)
        flash("CREATED SUCCESSFULY")
    return render_template('newCourse.html', title='Add Course', form=form)


@app.route('/addclass', methods=['GET', 'POST'])
@login_required
def addClass():
    if current_user.type != 'Admin':
        abort(403)
    # Create a new form
    form = CreateClass()
    # Get list of courses, classes for using as choices in the drop down boxes.
    courseList = courses()
    classList = classes()
    # Loop through each of these lists adding to the dictionaries for each
    # choice.
    courseChoices = [(course.courseID, course.title) for course in courseList]
    preReqChoices = [(item.classID, item.title) for item in classList]
    # This will loop through the list of available trainers and add them to
    # the choices.
    trainerChoices = [(item.trainerID, item.name)
                      for item in checkTrainer(session['classDate'])]
    # This will loop through the available rooms and add them to the choices.
    roomChoices = [(item.roomID, item.roomCode + " " + item.building + item.location)
                   for item in checkRoom(session['classDate'])]

    # Allocate each of the choices to the form.

    form.course.choices = courseChoices
    form.preReqs.choices = preReqChoices
    form.trainer.choices = trainerChoices
    form.room.choices = roomChoices

    # If a post request is made
    if request.method == 'POST':
        # Empty waiting list to create a new class with
        waitList = []
        # Join of the characters from the reqFac array and combine them into
        # one string.
        reqFacilities = ''.join(form.reqFac.data)
        # Loop through all of the classID's in the array to get a list of class
        # objects.
        preReqList = []
        for classid in form.preReqs.data:
            classObj = classes(classID=classid)
            preReqList.append(classObj)
        if form.validate_on_submit():
            addNewClass(form.course.data, preReqList, form.title.data, form.description.data,
                        form.capacity.data, form.room.data, form.trainer.data, waitList, session['classDate'], form.duration.data, reqFacilities)
            flash("CREATED SUCCESSFULY")
        else:
            flash("Error")
    return render_template('newClass.html', title='Add Class', form=form)


@app.route('/addclassdate', methods=['GET', 'POST'])
@login_required
def addClassDate():
    if current_user.type != 'Admin':
        abort(403)
    # Create a new form
    form = CreateClassDate()
    # If a post request is made
    if request.method == 'POST':
        if form.validate_on_submit():
            # Try and create a date object for given form data.
            try:
                classDate = datetime(
                    form.dateYear.data, form.dateMonth.data, form.dateDay.data, form.dateHour.data, 00)
                session['classDate'] = classDate
                return redirect('/addclass')
            # If this fails it will flash the error on screen.
            except:
                flash("Please enter a valid date")
    return render_template('newClassDate.html', title='Add Class', form=form)

# View a list of delegates.
# Only valid for admins.
@app.route('/delegates')
@login_required
def delList():
    if current_user.type != 'Admin':
        abort(403)
    delList = delegates()
    return render_template('delegates.html', title='Delegate List', delList=delList)

# View the schedule of a delegate.
# Only valid for admins.
@app.route('/delegates/<id>')
@login_required
def delSchedule(id):
    delid = id
    if current_user.type != 'Admin':
        abort(403)

    user = delegates(delID=delid)
    delClassList = user.classList

    return render_template('delsSched.html', title='Delegate Schedule', user=user, delClassList=delClassList)

# Sign up a delegate for a class, provided they meet requirements.
@app.route('/signup/<id>')
@login_required
def signUp(id):
    classID = id
    thisClass = classes(classID=id)
    if current_user.type == 'Delegate':
        if meetsRequirements(current_user, thisClass):
            if noTimeTableClash(current_user, thisClass):
                addToClass(thisClass, current_user)
                flash("You have been added.")
            else:
                flash("Cannot sign up. This module clashes with another class.")
        else:
            flash("You don't meet the requirements")
    else:
        flash("You are not authorised to do this")
    return redirect('/browse/classes/class/' + classID)

@app.route('/browse/classes/class/<id>')
def viewClassDetails(id):
    classID = id
    current_class = classes(classID=classID)
    classSize = classAttendenceLen(current_class)
    if current_user.is_authenticated:
        if current_user.type == 'Delegate':
            clash = noTimeTableClash(current_user, current_class)
            userQualify = meetsRequirements(current_user, current_class)
        else:
            userQualify = False
            clash = "NA"
    else:
        userQualify = "Sign"
        clash = "NA"
    return render_template('viewClass.html', title="Course", current_class=current_class, classSize=classSize, userQualify=userQualify, clash = clash)

# Cancel an upcoming class.
@app.route('/function/cancel/<classID>')
def cancelClass(classID):
    current_class = classes(classID=classID)
    removeFromClass(current_class, current_user)
    return redirect('/timetable')


# Send a reminder email about an upcoming class.
@app.route('/function/remind/<classID>')
def remindClass(classID):
    current_class = classes(classID=classID)
    reminderEmail(current_class, current_user)
    return redirect('/timetable')

# Delete a room with given ID.
@app.route('/deleteroom/<id>')
def deleteRoom(id):
    room = rooms(roomID=id)
    if delRoom(room):
        return redirect('/rooms')
    else:
        flash("Classes have been scheduled in this room")
        return redirect('/rooms/'+id)
