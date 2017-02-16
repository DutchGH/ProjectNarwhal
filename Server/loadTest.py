from app import db, models
import datetime


def addNewAdmin( ID, Name, Username, Password ):
    x = models.Admin(adminID=ID,name=Name,username=Username,password=Password)
    db.session.add(x)
    db.session.commit()

def addNewTrainer( ID, Name, Address, Phone, Email, Username, Password ):
    x = models.Trainer(trainerID=ID,name=Name,address=Address,phone=Phone,email=Email,username=Username,password=Password)
    db.session.add(x)
    db.session.commit()

def addNewRoom( ID, Capacity, RoomType, AccessRating, Location ):
    x = models.Room(roomID=ID,capacity=Capacity,roomType=RoomType,accessRating=AccessRating,location=Location)
    db.session.add(x)
    db.session.commit()

def addNewClass( ID, CourseID, Title, Description, Capacity, Location, Trainer ,waitList):
    x = models.Class(classID=ID,courseID=CourseID,title=Title,description=Description,capacity=Capacity,locationPoint=Location,trainerPoint=Trainer,waitList=waitList)
    db.session.add(x)
    db.session.commit()

def addNewDel( ID, Name, Username, Password, Class ):
    x = models.Delegate(delID=ID,name=Name,username=Username,password=Password,classList=Class)
    db.session.add(x)
    db.session.commit()

print("Creating admins.")
addNewAdmin(1,"Luke Roberts","Luke","pass");
addNewAdmin(2,"Jake Horsefield","Jake","pass")
addNewAdmin(3,"Jake Holland","Jake2","pass")

print("Creating trainers.")
addNewTrainer(1,"Sam Wilson","Dec-10",0,"swilson@leeds.ac.uk","sam1","pass")
addNewTrainer(2,"Eric Atwell","Dec-10",0,"eatwell@leeds.ac.uk","eric1","pass")
addNewTrainer(3,"Hamish Carr","Dec-10",0,"hcarr@leeds.ac.uk","hamish1","pass")

print("Creating rooms.")
addNewRoom(1,20,"Seminar Room","W","mt.1.6")
addNewRoom(2,100,"Lecture hall","W","mt.1.5")
addNewRoom(3,5,"Conference suite","W","mt.1.7")

print("Creating classes.")
rooms = models.Room.query.all()
trainers = models.Trainer.query.all()
delegates = models.Delegate.query.all()
addNewClass(1,2011,"Web App","Learn to use flask for creating a web server.",90,rooms[0].roomID,trainers[0].trainerID,delegates)
addNewClass(2,2121,"Data Mining","Mining through bare data and that.",90,rooms[1].roomID,trainers[1].trainerID,delegates)
addNewClass(3,2931,"Software Engineering","The art of developing software.",90,rooms[2].roomID,trainers[2].trainerID,delegates)

print("Creating Delegates.")
classes = models.Class.query.all()
addNewDel(1,"Ben Reed","Ben","pass",classes)
addNewDel(2,"Suhaib Saeed","Si","pass",classes)
addNewDel(3,"Jon-Fredick Henning","Jon","pass",classes)
print("DONE")
