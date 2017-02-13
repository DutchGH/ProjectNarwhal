from app import db, models

##Create some random db items
#room1 = models.Room(roomID=1,capacity=100,roomType"lecTheater",accessRating="W",location="N.1.3")

print("Creating admins.")
admin1 = models.Admin(adminID=1,name="Luke Roberts",username="Luke",password="pass")
admin2 = models.Admin(adminID=2,name="Jake Horsefield",username="Jake",password="pass")
admin3 = models.Admin(adminID=3,name="Jake Holland",username="Jake2",password="pass")

print("Creating trainers.")
train1 = models.Trainer(trainerID=1,name="Sam Wilson",address="Dec-10",phone=0,email="swilson@leeds.ac.uk",username="sam1",password="pass")
train2 = models.Trainer(trainerID=2,name="Eric Atwell",address="Dec-10",phone=0,email="eatwell@leeds.ac.uk",username="eric1",password="pass")
train3 = models.Trainer(trainerID=3,name="Hamish Carr",address="Dec-10",phone=0,email="hcarr@leeds.ac.uk",username="hamish1",password="pass")

print("Creating rooms.")
room1 = models.Room(roomID=1,capacity=20,roomType="Seminar Room",accessRating="W",location="mt.1.6")
room2 = models.Room(roomID=2,capacity=100,roomType="Lecture hall",accessRating="W",location="mt.1.5")
room3 = models.Room(roomID=3,capacity=5,roomType="Conference suite",accessRating="W",location="mt.1.7")


#db.session.add(room1,admin1)
print("Adding items to db.")
db.session.add(admin1)
db.session.add(admin2)
db.session.add(admin3)
db.session.add(train1)
db.session.add(train2)
db.session.add(train3)
db.session.add(room1)
db.session.add(room2)
db.session.add(room3)
db.session.commit()
print("DONE")
