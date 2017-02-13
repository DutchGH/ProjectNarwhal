from app import db, models

rooms = models.Room.query.all()
trainers = models.Trainer.query.all()
classes = models.Class.query.all()
dels = models.Delegate.query.all()
admin = models.Admin.query.all()

items = 0

print("Removing admins")
while(len(admin) > 0):
	c = len(admin) - 1
	item = admin[c]
	db.session.delete(item)
	db.session.commit()
	admin = models.Admin.query.all()
	items += 1
print("Removing trainers")
while(len(trainers) > 0):
	c = len(trainers) - 1
	item = trainers[c]
	db.session.delete(item)
	db.session.commit()
	trainers = models.Trainer.query.all()
	items += 1
print("Removing rooms")
while(len(rooms) > 0):
	c = len(rooms) - 1
	item = rooms[c]
	db.session.delete(item)
	db.session.commit()
	rooms = models.Room.query.all()
	items += 1
print("DONE")
print("Removed "+str(items)+" database items.")
