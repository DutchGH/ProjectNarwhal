from app import models,db
import datetime

#Return the list of classes
def classes( ID = "", CourseID = "", StartTime = "", ReqFac = "", PreTrain = "", Location = "", Trainer = "" ):
    test =""
    if ID != "":
        #This will return a single class based on ID.
        #q = models.Class.query.filter_by( classID = ID )
        test = test+"classID = "+str(ID)+","
    if CourseID != "":
        #This will return a list of classes under the same course.
        #q = models.Class.query.filter_by( courseID = CourseID )
        test = test+"courseID = "+str(CourseID)+","
    if StartTime != "":
        #This will return a list of classes starting a the same time.
        #q = models.Class.query.filter_by( startTime = StartTime )
        test = test+"startTime = "+str(StartTime)+","
    if ReqFac != "":
        #This will return a list of classes requiring certain facilities.
        #q = models.Class.query.filter_by( reqFac = ReqFac )
        test = test+"reqFac = "+str(ReqFac)+","
    if PreTrain != "":
        #This will return a list of classes requiring other courses.
        #q = models.Class.query.filter_by( preTrain = PreTrain )
        test = test+"preTrain = "+str(PreTrain)+","
    if Location != "":
        #This will return a list of classes at a certain location.
        #q = models.Class.query.filter_by( location = Location )
        test = test+"location = "+str(Location)+","
    if Trainer != "":
        #This will return a list of classes taught by a certain trainer.
        #q = models.Class.query.filter_by( trainer = Trainer )
        test = test+"trainer = "+str(Trainer)

    print( test )

    #q = models.Class.query.filter_by( eval( test ))
    q = []
    #This will ensure the function returns the item instead of a list of one.
    if(len(q) == 1):
         q = q[0]
    return q

#Return a list of all trainers
def trainers():
    return models.Trainer.query.all()

#Return a list of delegates based on a query.
def delegates( name = "None" ):
    if type(name) == int:
        #This will return a single user based on ID.
        q = models.Delegate.query.filter_by( delID = name )
    elif type(name) == str:
        #This will return a single user based on username.
        q = models.Delegate.query.filter_by( username = name )
    elif name == "None":
        q = models.Delegate.query.all()

    #This will ensure the function returns the item instead of a list of one.
    if(q.count() == 1):
        q = q[0]
    return q

#Return a list of all admins
def admins():
    return models.Admin.query.all()

#Returns a list of all rooms
def rooms():
    return models.Rooms.query.all()

#Adds an item to a list
def addToList(list,item):
    list

#This will add a new admin to the Admin database.
def addNewAdmin( ID, Name, Username, Password ):
    x = models.Admin(adminID=ID,name=Name,username=Username,password=Password)
    db.session.add(x)
    db.session.commit()

#This will add a new Trainer to the trainer database.
def addNewTrainer( ID, Name, Address, Phone, Email, Username, Password ):
    x = models.Trainer(trainerID=ID,name=Name,address=Address,phone=Phone,email=Email,username=Username,password=Password)
    db.session.add(x)
    db.session.commit()

#This will add a new room to the room database.
def addNewRoom( ID, Capacity, RoomType, AccessRating, Location ):
    x = models.Room(roomID=ID,capacity=Capacity,roomType=RoomType,accessRating=AccessRating,location=Location)
    db.session.add(x)
    db.session.commit()

#This will add a new class to the class database.
def addNewClass( ID, CourseID, Title, Description, Capacity, Location, Trainer ,waitList):
    x = models.Class(classID=ID,courseID=CourseID,title=Title,description=Description,capacity=Capacity,locationPoint=Location,trainerPoint=Trainer,waitList=waitList)
    db.session.add(x)
    db.session.commit()

#This will add a new delegate to the delegate database.
def addNewDel( ID, Name, Username, Password, Class ):
    x = models.Delegate(delID=ID,name=Name,username=Username,password=Password,classList=Class)
    db.session.add(x)
    db.session.commit()
