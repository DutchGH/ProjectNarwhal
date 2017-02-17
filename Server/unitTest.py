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
    oldRoomList = rooms().count()
    newRoom = addNewRoom(999,999,"TestRoom","All","Nowhere")
    newRoomList = rooms().count()
    db.session.delete(newRoom)
    db.session.commit()
    return newRoomList - oldRoomList

################################################################################
#Below is the actual test function, here tests are performed and there expected
#outcomes declared.
################################################################################

class TestCase( unittest.TestCase ):
    def setUp( self ):
        #Add anything you need for these tests to run here.
        print("Nothing to set up.")

    def tearDown( self ):
        #Remove anything you added in the setUp() function here.
        print("Nothing to tear down.")

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

if __name__ == '__main__':
    unittest.main()
