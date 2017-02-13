from app import db, models

rooms = models.Room.query.all()
trainers = models.Trainer.query.all()
classes = models.Class.query.all()
dels = models.Delegate.query.all()
admin = models.Admin.query.all()

adminItems = 0
trainerItems = 0
roomItems = 0
classItems = 0
delegateItems = 0

print("Removing admins")
while(len(admin) > 0):
	c = len(admin) - 1
	item = admin[c]
	db.session.delete(item)
	db.session.commit()
	admin = models.Admin.query.all()
	adminItems += 1
print("Removing trainers")
while(len(trainers) > 0):
	c = len(trainers) - 1
	item = trainers[c]
	db.session.delete(item)
	db.session.commit()
	trainers = models.Trainer.query.all()
	trainerItems += 1
print("Removing rooms")
while(len(rooms) > 0):
	c = len(rooms) - 1
	item = rooms[c]
	db.session.delete(item)
	db.session.commit()
	rooms = models.Room.query.all()
	roomItems += 1
print("Removing classes")
while(len(classes) > 0):
	c = len(classes) - 1
	item = classes[c]
	db.session.delete(item)
	db.session.commit()
	classes = models.Class.query.all()
	classItems += 1
print("Removing delegates")
while(len(dels) > 0):
	c = len(dels) - 1
	item = dels[c]
	db.session.delete(item)
	db.session.commit()
	dels = models.Delegate.query.all()
	delegateItems += 1
print("DONE")
print("Removed "+str(adminItems)+" items from admin database.")
print("Removed "+str(trainerItems)+" items from trainer database.")
print("Removed "+str(roomItems)+" items from room database.")
print("Removed "+str(classItems)+" items from class database.")
print("Removed "+str(delegateItems)+" items from delegate database.")
