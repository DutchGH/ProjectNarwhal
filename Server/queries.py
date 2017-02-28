from app import models,db
import datetime

#Converts a query object into lists or a single item if only one is returned.
def listConvert( x ):
    if( x.count() == 1 ):
         x = x[0]
         return x
    else:
        y = []
    for i in x:
        y.append(i)
    return y

#Return the list of classes
def classes( **kwargs ):
    q = models.Class.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

#Return the list of courses
def courses( **kwargs ):
    q = models.Course.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

#Return a list of all trainers
def trainers( **kwargs ):
    q = models.Trainer.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

#Return a list of delegates based on a query.
def delegates( **kwargs ):
    q = models.Delegate.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

#Return a list of all admins
def admins( **kwargs ):
    q = models.Admin.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

#Returns a list of all rooms
def rooms( **kwargs ):
    q = models.Room.query.filter_by(**kwargs)
    q = listConvert(q)
    return q

#Adds an item to a list, works to add either classes to a delegates classList or
#to add delegates to a classes waiting list.
def addToList( list,item ):
    #If adding to a waiting list
    if(list.__tablename__ == 'Class'):
        list.waitList.append( item )
    #If adding to a class list
    else:
        list.classList.append( item )
    db.session.commit()

#Checks for unique username. Returns false if the username is taken.
def checkUserName( name ):
    dels = delegates()
    for i in dels:
        if( i.username == name ):
            return False
    return True

#Returns the delegates taking a class
def classAttendence( thisClass ):
    dels=delegates()
    at = []
    for i in dels:
        for g in i.classList:
            if g.classID == thisClass.classID:
                at.append( g )
    return at

#Returns the number of delegates taking a class
def classAttendenceLen( thisClass ):
    return len( classAttendence( thisClass ) )

#Checks if a class is at capacity
def capacity( thisClass ):
    if( thisClass.capacity >= ( classAttendenceLen( thisClass ) ) ):
        return False
    else:
        return True

#Removes an item from the database
def remove(item):
    db.session.delete(item)

#This will add a new admin to the Admin database.
def addNewAdmin(Name, Username, Password):
    ID = genID(admins)
    x = models.Admin(adminID=ID,name=Name,username=Username,password=Password)
    db.session.add(x)
    db.session.commit()
    return x

#This will add a new Trainer to the trainer database.
def addNewTrainer(Name, Address, Phone, Email, Username, Password):
    ID = genID(trainers)
    x = models.Trainer(trainerID=ID,name=Name,address=Address,phone=Phone,
    email=Email,username=Username,password=Password)
    db.session.add(x)
    db.session.commit()
    return x

#This will add a new room to the room database.
def addNewRoom(Capacity, RoomType, AccessRating, Location):
    ID = genID(rooms)
    x = models.Room(roomID=ID,capacity=Capacity,roomType=RoomType,
    accessRating=AccessRating,location=Location)
    db.session.add(x)
    db.session.commit()
    return x

#This will add a new class to the class database.
def addNewClass(CourseID, Title, Description, Capacity, Location, Trainer ,
waitList):
    ID = genID(classes)
    x = models.Class(classID=ID,coursePoint=CourseID,title=Title,description=
    Description,capacity=Capacity,locationPoint=Location,trainerPoint=Trainer,
    waitList=waitList)
    db.session.add(x)
    db.session.commit()
    return x

def addNewCourse(Title,Description):
    ID = genID(courses)
    x = models.Course(courseID = ID, title=Title, description=Description)
    db.session.add(x)
    db.session.commit()
    return x

#This will add a new delegate to the delegate database.
def addNewDel(Name, Username, Password, Class):
    ID = genID(delegates)
    x = models.Delegate(delID=ID,name=Name,username=Username,password=Password,
    classList=Class)
    db.session.add(x)
    db.session.commit()
    return x

#This will generate a unique ID for a new database entry.
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
        if ( modelType == models.Admin or modelType == models.Trainer or modelType == models.Delegate ):
            if (delegates( delID = ID ) == [] and trainers( trainerID = ID) == [] and admins( adminID = ID ) == []):
                return ID
        elif modelType == models.Room:
            if (model( roomID = ID ) == []):
                return ID
        elif modelType == models.Class:
            if (model( classID = ID ) == []):
                return ID
        elif modelType == models.Course:
            if (model( courseID = ID ) == []):
                return ID
        ID += 1
