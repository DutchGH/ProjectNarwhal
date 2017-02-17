import os
import unittest
from app import db, models
from queries import *

################################################################################
#Place the functions used to perform tests below.
################################################################################
def addRoom():
    oldRoomList = models.Room.query.all()
    newRoom = models.Room(roomID=999,capacity=999,roomType="TestRoom",
    accessRating="All",location="Nowhere")
    db.session.add(newRoom)
    db.session.commit()
    newRoomList = models.Room.query.all()
    db.session.delete(newRoom)
    db.session.commit()
    return len(newRoomList) - len(oldRoomList)

def addRoomQuick():
    oldRoomList = len(rooms())
    newRoom = addNewRoom(999,999,"TestRoom","All","Nowhere")
    newRoomList = len(rooms())
    db.session.delete(newRoom)
    db.session.commit()
    return newRoomList - oldRoomList

def addTrainer():
    oldTrainerList = models.Trainer.query.all()
    newTrainer = models.Trainer(trainerID=999,name="Test")
    db.session.add(newTrainer)
    db.session.commit()
    newTrainerList = models.Trainer.query.all()
    db.session.delete(newTrainer)
    db.session.commit()
    return len(newTrainerList) - len(oldTrainerList)

def addTrainerQuick():
    oldTrainerList = len(trainers())
    newTrainer = addNewTrainer(999,"Sam Wilson","Dec-10",0,"swilson@leeds.ac.uk",
    "sam1","pass")
    newTrainerList = len(trainers())
    db.session.delete(newTrainer)
    db.session.commit()
    return newTrainerList - oldTrainerList

def addAdmin():
    oldAdminList = models.Admin.query.all()
    newAdmin = models.Admin(adminID=999,name="Test")
    db.session.add(newAdmin)
    db.session.commit()
    newAdminList = models.Admin.query.all()
    db.session.delete(newAdmin)
    db.session.commit()
    return len(newAdminList) - len(oldAdminList)

def addAdminQuick():
    oldAdminList = len(admins())
    newAdmin = addNewAdmin(999,"Luke Roberts","Luke","pass");
    newAdminList = len(admins())
    db.session.delete(newAdmin)
    db.session.commit()
    return newAdminList - oldAdminList

def addDel():
    oldDelList = models.Delegate.query.all()
    newDel = models.Delegate(delID=999,name="Test")
    db.session.add(newDel)
    db.session.commit()
    newDelList = models.Delegate.query.all()
    db.session.delete(newDel)
    db.session.commit()
    return len(newDelList) - len(oldDelList)

def addDelQuick():
    oldDelList = len(delegates())
    newDel = addNewDel(999,"Ben Reed","Ben","pass",classes())
    newDelList = len(delegates())
    db.session.delete(newDel)
    db.session.commit()
    return newDelList - oldDelList

def addClass():
    oldClassList = models.Class.query.all()
    newClass = models.Class(classID=999)
    db.session.add(newClass)
    db.session.commit()
    newClassList = models.Class.query.all()
    db.session.delete(newClass)
    db.session.commit()
    return len(newClassList) - len(oldClassList)

def addClassQuick():
    oldClassList = len(classes())
    newClass = addNewClass(999,2011,"Web App","Learn to use flask for creating a web server.",90,rooms()[0].roomID,trainers()[0].trainerID,delegates())
    newClassList = len(classes())
    db.session.delete(newClass)
    db.session.commit()
    return newClassList - oldClassList
################################################################################
#Below is the actual test function, here tests are performed and there expected
#outcomes declared.
################################################################################

class TestCase( unittest.TestCase ):
    #def setUp( self ):
        #Add anything you need for these tests to run here.
        #print("Nothing to set up.")

    #def tearDown( self ):
        #Remove anything you added in the setUp() function here.
        #print("Nothing to tear down.")

    ############################################################################
    #Add the tests and their expected outcomes below.
    ############################################################################

    #Test that rooms can be added to the database.
    def testRoomAddition( self ):
        assert addRoom() == 1

    #Test that rooms can be added to the database using functions from the
    #queries library.
    def testShortRoomAddition( self ):
        assert addRoomQuick() == 1

    #Test that trainers can be added to the database.
    def testTrainerAddition( self ):
        assert addTrainer() == 1

    #Test that trainers can be added to the database using functions from the
    #queries library.
    def testShortTrainerAddition( self ):
        assert addTrainerQuick() == 1

    #Test that admins can be added to the database.
    def testAdminAddition( self ):
        assert addAdmin() == 1

    #Test that admins can be added to the database using functions from the
    #queries library.
    def testShortAdminAddition( self ):
        assert addAdminQuick() == 1

    #Test that delegates can be added to the database.
    def testDelAddition( self ):
        assert addDel() == 1

    #Test that delegates can be added to the database using functions from the
    #queries library.
    def testShortDelAddition( self ):
        assert addDelQuick() == 1

    #Test that classes can be added to the database.
    def testClassAddition( self ):
        assert addClass() == 1

    #Test that classes can be added to the database using functions from the
    #queries library.
    def testShortClassAddition( self ):
        assert addClassQuick() == 1

if __name__ == '__main__':
    unittest.main()
