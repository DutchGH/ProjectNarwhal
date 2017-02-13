from app import db
import datetime
from sqlalchemy import Column, Integer, DateTime

##Trainer
class Trainer(db.Model):
	__tablename__ = 'Trainer'
	trainerID = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	address = db.Column(db.String(100))
	phone = db.Column(db.Integer)
	email = db.Column(db.String(100))
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))

##Admin
class Admin(db.Model):
	__tablename__ = 'Admin'
	adminID = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))

##Room
class Room(db.Model):
	__tablename__ = 'Room'
	roomID = db.Column(db.Integer,primary_key=True)
	capacity = db.Column(db.Integer)
	roomType = db.Column(db.String(100))
	picURL = db.Column(db.String(100))
	accessRating = db.Column(db.String(100))
	location = db.Column(db.String(100))

##Course
class Class(db.Model):
	__tablename__ = 'Class'
	classID = db.Column(db.Integer,primary_key=True)
	courseID = db.Column(db.Integer)
	title = db.Column(db.String(100))
	description = db.Column(db.String(100))
	capacity = db.Column(db.Integer)
	startTime = db.Column(db.DateTime)
	duration = db.Column(db.Integer)
	requiredFacilities = db.Column(db.String(100))
	prerequsitTraining = db.Column(db.String(100))
	locationPoint = db.Column(db.Integer, db.ForeignKey('Room.roomID'))
	location = db.relationship("Room",foreign_keys=[locationPoint])
	trainerPoint = db.Column(db.Integer, db.ForeignKey('Trainer.trainerID'))
	waitListPoint = db.Column(db.Integer, db.ForeignKey('Delegate.delID'))
	trainer = db.relationship("Trainer",foreign_keys=[trainerPoint])
	waitList = db.relationship("Delegate",foreign_keys=[waitListPoint])

##Delegates
class Delegate(db.Model):
	__tablename__ = 'Delegate'
	delID = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))
	classListPoint = db.Column(db.Integer, db.ForeignKey('Class.classID'))
	classList= db.relationship("Class",foreign_keys=[classListPoint])
