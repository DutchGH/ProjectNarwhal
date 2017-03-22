from app import models, db
import datetime


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

# Checks for unique username. Returns false if the username is taken.


def checkUserName(name):
    dels = delegates()
    for i in dels:
        if(i.username == name):
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

# This will add a new room to the room database.


def addNewRoom(Capacity, RoomType, AccessRating, RoomCode, Building, Location):
    ID = genID(rooms)
    x = models.Room(roomID=ID, capacity=Capacity, roomType=RoomType,
                    accessRating=AccessRating, location=Location, building=Building,
                    roomCode=RoomCode)
    db.session.add(x)
    db.session.commit()
    return x

# This will add a new class to the class database.


def addNewClass(CourseID, Title, Description, Capacity, Location, Trainer,
                waitList):
    ID = genID(classes)
    x = models.Class(classID=ID, coursePoint=CourseID, title=Title,
                     description=Description, capacity=Capacity, locationPoint=Location,
                     trainerPoint=Trainer, waitList=waitList)
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

# A function that adds a delegate to a classes attendanceList or
# waitingList, depending on capacity


def addToClass(thisClass, x):
    if(len(thisClass.attendanceList) < thisClass.capacity):
        thisClass.attendanceList.append(x)
    else:
        print("In second bit")
        thisClass.waitList.append(x)
    db.session.commit()

# A function that checks a classes prerequists against a delegates history

# A function for removing entries


def removeItem(item):
    db.session.delete(item)
    db.session.commit()

# A query for editing entries (doesn't work yet)
# def edit( item, **kwargs ):
#    for field, value in kwargs.items():
#        setattr(item,str(field),value)
#    db.session.commit()

# A function which removes a user from a classList and moves someone over
# from the waitingList


def removeFromClass(thisClass, delegate):
    thisClass.attendanceList.remove(delegate)
    if(len(thisClass.waitList) > 0):
        thisClass.attendanceList.append(thisClass.waitList[0])
        thisClass.waitList.remove(thisClass.waitList[0])
    db.session.commit()
