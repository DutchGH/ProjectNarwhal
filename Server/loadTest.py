from app import db, models
from queries import *


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

print("Creating courses.")
addNewCourse(0,"Computer Science","The best course ever!")
addNewCourse(1,"French","Not the best course ever!")
addNewCourse(2,"English","Really not the best course ever!")

print("Creating classes.")
rooms = models.Room.query.all()
trainers = models.Trainer.query.all()
delegates = models.Delegate.query.all()
courses = models.Course.query.all()
addNewClass(1,courses[0].courseID,"Web App","Learn to use flask for creating a web server.",90,rooms[0].roomID,trainers[0].trainerID,delegates)
addNewClass(2,courses[0].courseID,"Data Mining","Mining through bare data and that.",90,rooms[1].roomID,trainers[1].trainerID,delegates)
addNewClass(3,courses[1].courseID,"Software Engineering","The art of developing software.",90,rooms[2].roomID,trainers[2].trainerID,delegates)

print("Creating delegates.")
classes = models.Class.query.all()
addNewDel(1,"Ben Reed","Ben","pass",classes)
addNewDel(2,"Suhaib Saeed","Si","pass",classes)
addNewDel(3,"Jon-Fredick Henning","Jon","pass",classes)

print("DONE")
