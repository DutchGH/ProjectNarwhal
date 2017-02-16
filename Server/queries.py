from app import models,db

#Return the list of classes
def classes():
    return models.Class.query.all()

#Return a list of all trainers
def trainers():
    return models.Trainer.query.all()

#Return a list of all delegates
def delegates():
    return models.Delegate.query.all()

#Return a list of all admins
def admins():
    return models.Admin.query.all()

#Returns a list of all rooms
def rooms():
    return models.Rooms.query.all()

#Adds an item to a list
def addToList(list,item):
    list
