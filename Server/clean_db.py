from app import db, models

rooms = models.Room.query.all()
trainers = models.Trainer.query.all()
classes = models.Class.query.all()
dels = models.Delegate.query.all()
admin = models.Admin.query.all()

items = 0

while(len(admin) > 0):
	print("Removing admins")
	c = len(admin) - 1
	item = admin[c]
	db.session.delete(item)
	db.session.commit()
	admin = models.Admin.query.all()
	items += 1

print("DONE")
print("Removed "+str(items)+" database items.")
