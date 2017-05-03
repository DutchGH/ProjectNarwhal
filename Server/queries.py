from flask import Flask
from app import models,db, mail
from flask_mail import Message
from datetime import *


# Converts a query object into lists or a single item if only one is returned.
def listConvert(x):
    if(x.count() == 1):
        x = x[0]
        return x
    else:
        y = []
    for i in x:
        y.append(i)
    return y

# Return the list of classes


def classes(**kwargs):
    q = models.Class.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

# Return the list of courses


def courses(**kwargs):
    q = models.Course.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

# Return a list of all trainers


def trainers(**kwargs):
    q = models.Trainer.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

# Return a list of delegates based on a query.


def delegates(**kwargs):
    q = models.Delegate.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

# Return a list of all admins


def admins(**kwargs):
    q = models.Admin.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

# Returns a list of all rooms


def rooms(**kwargs):
    q = models.Room.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

# Adds an item to a list, works to add either classes to a delegates classList or
# to add delegates to a classes waiting list.


def addToList(list, item):
    # If adding to a waiting list
    if(list.__tablename__ == 'Class'):
        list.waitList.append(item)
    # If adding to a class list
    else:
        list.classList.append(item)
    db.session.commit()


#Checks for unique username. Returns false if the username is taken.
def checkUserName( name ):
    if delegates( username = name ) != []:
        return False
    if trainers( username = name ) != []:
        return False
    if admins( username = name ) != []:
        return False
    return True

# Returns the delegates taking a class
def classAttendence(thisClass):
    dels = delegates()
    at = []
    for i in dels:
        for g in i.classList:
            if g.classID == thisClass.classID:
                at.append(g)
    return at

# Returns the number of delegates taking a class
def classAttendenceLen(thisClass):
    return len(classAttendence(thisClass))

# Checks if a class is at capacity
def capacity(thisClass):
    if(thisClass.capacity >= (classAttendenceLen(thisClass))):
        return False
    else:
        return True

# This will add a new admin to the Admin database.
def addNewAdmin(Name, Username, Password, Email):
    ID = genID(admins)
    x = models.Admin(adminID=ID, name=Name, username=Username,
                     password=Password, email=Email)
    db.session.add(x)
    db.session.commit()
    return x

# This will add a new Trainer to the trainer database.
def addNewTrainer(Name, Address, Phone, Email, Username, Password):
    ID = genID(trainers)
    x = models.Trainer(trainerID=ID, name=Name, address=Address,
                       phone=Phone, email=Email, username=Username, password=Password)
    db.session.add(x)
    db.session.commit()
    return x

#This will add a new room to the room database.
def addNewRoom(Capacity, RoomType, AccessRating, RoomCode, Fac, Building, Location):
    ID = genID(rooms)
    x = models.Room(roomID = ID, capacity = Capacity, roomType = RoomType,
    accessRating = AccessRating, location = Location, facilities = Fac, building = Building,
    roomCode = RoomCode)
    db.session.add(x)
    db.session.commit()
    return x

#This will add a new class to the class database.
def addNewClass(CourseID, preReqs, Title, Description, Capacity, Location, Trainer,
waitList, StartDate, duration, reqFac = None):
    ID = genID(classes)
    EndDate = StartDate+timedelta(weeks=duration)+timedelta(hours=1)
    x = models.Class(classID = ID, preTrain = preReqs, coursePoint = CourseID, title = Title,
    description = Description, capacity = Capacity, locationPoint = Location,
    trainerPoint = Trainer, waitList = waitList, startDate = StartDate, reqFac = reqFac,
    duration = duration, endDate = EndDate)
    db.session.add(x)
    db.session.commit()
    return x


def addNewCourse(Title, Description):
    ID = genID(courses)
    x = models.Course(courseID=ID, title=Title, description=Description)
    db.session.add(x)
    db.session.commit()
    return x

# This will add a new delegate to the delegate database.
def addNewDel(Name, Username, Password, Class, Email):
    ID = genID(delegates)
    x = models.Delegate(delID=ID, name=Name, username=Username,
                        password=Password, classList=Class, email=Email)
    db.session.add(x)
    db.session.commit()
    return x

# This will generate a unique ID for a new database entry.
def genID(model):
    modelList = model()
    try:
        if modelList == []:
            return 0
        ID = len(modelList)
    except:
        return 1

    modelType = type(model()[0])
    found = False
    while found == False:
        if (modelType == models.Admin or modelType == models.Trainer or
                modelType == models.Delegate):
            if (delegates(delID=ID) == [] and trainers(trainerID=ID) ==
                    [] and admins(adminID=ID) == []):
                return ID
        elif modelType == models.Room:
            if (model(roomID=ID) == []):
                return ID
        elif modelType == models.Class:
            if (model(classID=ID) == []):
                return ID
        elif modelType == models.Course:
            if (model(courseID=ID) == []):
                return ID
        ID += 1

# A function that identifies a user as a delegate, a trainer or an adminID
def checkUser(user):
    if(type(user) == models.Delegate):
        return "Delegate"
    elif(type(user) == models.Admin):
        return "Admin"
    elif(type(user) == models.Trainer):
        return "Trainer"
    return "INVALID"

# A function that adds a delegate to a classes attendanceList or waitingList, depending on capacity
def addToClass(thisClass,thisDel):
    if(len(thisClass.attendanceList) < thisClass.capacity):
        thisClass.attendanceList.append(thisDel)
        confirmEmail(thisClass,thisDel)
    else:
        print("In second bit")
        thisClass.waitList.append(thisDel)
        waitingEmail(thisClass,thisDel)
    db.session.commit()

#Will send an email to the user email address confirming their place on the course.
def confirmEmail(thisClass,thisDel):
    time = thisClass.startDate
    time = time.strftime("%H:%M, %d/%m/%y")
    message = Message("Hi %s" % thisDel.name, sender = "luketestacc.gmail.com", recipients = [thisDel.email])
    message.body = "This email is confirming your place on the class -" + thisClass.title + " commencing on " + time + "."
    mail.send(message)

#Will send an email to the user email address notfying them they have been put on a waiting list.
def waitingEmail(thisClass,thisDel):
    message = Message("Hi %s" % thisDel.name, sender = "luketestacc.gmail.com", recipients = [thisDel.email])
    message.body = "The course "  + thisClass.title + " is currently full you have been placed on a waiting list. You will automatically be moved on to the course if a place becomes available, and will receive an email confirming."
    mail.send(message)

# A function for removing entries
def removeItem(item):
    db.session.delete(item)
    db.session.commit()

# A query for editing entries
def edit( item, **kwargs ):
    for field, value in kwargs.items():
        setattr(item,str(field),value)
    db.session.commit()

# A function which removes a user from a classList and moves someone over
# from the waitingList
def removeFromClass(thisClass, delegate):
    thisClass.attendanceList.remove(delegate)
    if(len(thisClass.waitList) > 0):
        thisClass.attendanceList.append(thisClass.waitList[0])
        thisClass.waitList.remove(thisClass.waitList[0])
        confirmEmail(thisClass,delegate)
    db.session.commit()

# A function that recovers a list of classes yet to be taught.
def futureClasses():
    # Get the current time.
    today = datetime.now()
    # Get a list of all classes
    classList = classes()
    # Go through all the classes, removing any that have already happened
    for i in classList:
        if(i.endDate < today):
            classList.remove(i)
    # Return the result
    return classList

# A function that recovers a list of classes already taught.
def pastClasses():
    # Get the current time.
    today = datetime.now()
    # Get a list of all classes
    classList = classes()
    # Go through all the classes, removing any that are yet to happen.
    for i in classList:
        if (i.endDate > today):
            classList.remove(i)
    # Return the result
    return classList

# A function that recovers a list of classes already taught, from a delegates
# classList.
def history(delegate):
    # Get the current time.
    today = datetime.now()
    # Get a list of all classes
    classList = delegate.classList
    # Go through all the classes, removing any that are yet to happen.
    for i in classList:
        if (i.endDate > today):
            classList.remove(i)
    # Return the result
    return classList

# A function that recovers a list of classes a delegate is yet to take.
def schedule(delegate):
    # Get the current time.
    today = datetime.now()
    # Get the classList
    classList = delegate.classList
    # Go through all the classes, removing any that have already happened
    for i in classList:
        if(i.endDate < today):
            classList.remove(i)
    # Return the result
    return classList

# Function that checks a rooms accessRating, returning an array of properties.
def checkAccess(rating):
    accessRating = []
    if 'A' in rating:
        accessRating.append("Assistive learning system.")
    if 'L' in rating:
        accessRating.append("Level access.")
    if 'W' in rating:
        accessRating.append("Wheelchair access.")
    return accessRating

# Function that checks a room's facilities, returning an array of properties.
def checkFacilities(facilities):
    facList = []
    if 'M' in facilities:
        facList.append("Microphone.")
    if 'D' in facilities:
        facList.append("DVD player.")
    if 'P' in facilities:
        facList.append("Projector.")
    if 'I' in facilities:
        facList.append("Interactive white board.")
    if 'L' in facilities:
        facList.append("Lectern.")
    if 'C' in facilities:
        facList.append("Chalkboard.")
    if 'S' in facilities:
        facList.append("Computer suite.")

    return facList

# Function that returns a list of available trainers at a given time
def checkTrainer(time):
    # Get a list of trainers
    teachers = trainers()
    # A list of classes that conflict with the given time
    clashList = []
    # A list of all classes
    allClass = classes()
    # Go through each class and determine if it's a clashClass
    for i in allClass:
        # Get the range of sessions in this class
        for j in range(0,i.duration):
            if((i.startDate+timedelta(weeks = j) <= time) and ((i.startDate+timedelta(weeks = j)+timedelta(minutes = 60)) >= time)):
                clashList.append(i)
    # Go through each clashing class and get the teacher, remove it the teachers
    for j in clashList:
        teachers.remove(j.trainer)
    return teachers

# Function that returns a list of available rooms at a given time
def checkRoom(time):
    # Get a list of trainers
    classRooms = rooms()
    # A list of classes that conflict with the given time
    clashList = []
    # A list of all classes
    allClass = classes()
    # Go through each class and determine if it's a clashClass
    for i in allClass:
        # Get the range of sessions in this class
        for j in range(0,i.duration):
            if((i.startDate+timedelta(weeks = j) <= time) and ((i.startDate+timedelta(weeks = j)+timedelta(minutes = i.duration)) >= time)):
                clashList.append(i)
    # Go through each clashing class and get the room, remove it the classRooms
    for j in clashList:
        classRooms.remove(j.location)
    return classRooms

# Get a list of classes with the same course number
def getCourseClasses(thisCourse):
    preReqs = listConvert(models.Class.query.filter_by(course = thisCourse))
    if(type(preReqs) != type([])):
        preReqs = [preReqs]
    return preReqs

# Function that checks if a delegate meets the prerequists of a classRooms
def checkPrereq(delegate,thisClass):
    # Get the list of required classes for the class
    preReqs = thisClass.preTrain
    # Get the delegates history
    completedClasses = history(delegate)
    # A list of all non-met preReqs
    notMet = []
    # Go through all the preReqs and check if they are in the completedClasses
    # adding them to notMet if not.
    for i in preReqs:
        if((i in completedClasses) == False):
            notMet.append(i)
    return(notMet)

# Function that gives a simple True/False answer to whether or not a delegate hamish1
# met the prerequists for a class.
def meetsRequirements(delegate,thisClass):
    returnedList = checkPrereq(delegate,thisClass)
    if(len(returnedList) == 0):
        return True
    return False

# Function that returns the timetable for a given delegate
def timetable(delegate):
    # Get the non finished classes for this delegate.
     classList = schedule(delegate)
     lessons = []
     for i in classList:
         for j in range(0,i.duration):
             lessons.append([i.startDate+timedelta(weeks=j),i.title,i.trainer.name,i.location.location])
     # Sort the list by time
     lessons = sorted(lessons, key = lambda x: x[0])
     #Get the current datetime
     today = datetime.now()
     # Go through the classList and remove all classes gone
     for i in lessons:
         if(i[0] < today):
             lessons.remove(i)
     return lessons
