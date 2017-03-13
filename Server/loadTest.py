from app import db, models
from queries import *


print("Creating admins.")
addNewAdmin("Luke Roberts", "Luke", "pass", "LRoberts@email.com")
addNewAdmin("Jake Horsefield", "Jake", "pass", "JHorsefield@email.com")
addNewAdmin("Jake Holland", "Jake2", "pass", "JHolland@email.com")

print("Creating trainers.")
addNewTrainer("Sam Wilson", "Dec-10", 0, "swilson@leeds.ac.uk", "sam1", "pass")
addNewTrainer("Eric Atwell", "Dec-10", 0, "eatwell@leeds.ac.uk", "eric1", "pass")
addNewTrainer("Hamish Carr", "Dec-10", 0, "hcarr@leeds.ac.uk", "hamish1", "pass")

print("Creating rooms.")
addNewRoom(20, "Seminar Room", "W", "ES1", "EC Stoner", "Leeds")
addNewRoom(100, "Lecture hall", "W", "RS19", "Roger Stevens", "Leeds")
addNewRoom(5, "Conference suite", "W", "ES33", "EC Stoner", "Leeds")

print("Creating courses.")
addNewCourse("Computer Science", "The best course ever!")
addNewCourse("French", "Not the best course ever!")
addNewCourse("English", "Really not the best course ever!")

print("Creating classes.")
rooms = models.Room.query.all()
trainers = models.Trainer.query.all()
delegates = models.Delegate.query.all()
courses = models.Course.query.all()
addNewClass(courses[0].courseID, "Web App", "Learn to use flask for creating a web server.", 90, rooms[0].roomID, trainers[0].trainerID, delegates)
addNewClass(courses[0].courseID, "Data Mining", "Mining through bare data and that.", 90, rooms[1].roomID, trainers[1].trainerID, delegates)
addNewClass(courses[1].courseID, "Software Engineering", "The art of developing software.", 90, rooms[2].roomID, trainers[1].trainerID, delegates)

print("Creating delegates.")
classes = models.Class.query.all()
addNewDel("Ben Reed", "Ben", "pass", classes, "LRoberts@email.com")
addNewDel("Suhaib Saeed", "Si", "pass", classes, "SSaeed@email.com")
addNewDel("Jon-Fredick Henning", "Jon", "pass", classes, "JFHenning@email.com")

print("DONE")
