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

#Adds an item to a list, works to add either classes to a delegates classList or
#to add delegates to a classes waiting list.
def addToList( list,item ):
    #If adding to a waiting list
    if(list.__tablename__ == 'Class'):
        list.waitList.append( item )
    #If adding to a class list
    else:
        list.classList.append( item )
    db.session.commit()

#Checks for unique username. Returns false if the username is taken.
def checkUserName( name ):
    dels = delegates()
    for i in dels:
        if( i.username == name ):
            return False
    return True

#Returns the delegates taking a class
def classAttendence( thisClass ):
    dels=delegates()
    at = []
    for i in dels:
        for g in i.classList:
            if g.classID == thisClass.classID:
                at.append( g )
    return at

#Returns the number of delegates taking a class
def classAttendenceLen( thisClass ):
    return len( classAttendence( thisClass ) )

#Checks if a class is at capacity
def capacity( thisClass ):
    if( thisClass.capacity >= ( classAttendenceLen( thisClass ) ) ):
        return False
    else:
        return True

#Removes an item from the database
def remove(item):
    db.session.delete(item)
    db.session.commit()
