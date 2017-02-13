from app import db, models

##Create some random db items
#room1 = models.Room(roomID=1,capacity=100,roomType"lecTheater",accessRating="W",location="N.1.3")

print("Creating admins.")
admin1 = models.Admin(adminID=1,name="Luke Roberts",username="Luke",password="pass")


#db.session.add(room1,admin1)
print("Adding items to db.")
db.session.add(admin1)
db.session.commit()
print("DONE")
