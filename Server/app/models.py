from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

#Association table for the delegate's class lists.
association_table = db.Table('association_table', db.Model.metadata,
	db.Column('classID', db.Integer, db.ForeignKey('Class.classID')),
	db.Column('delID', db.Integer, db.ForeignKey('Delegate.delID'))
)


#Association table for the classes' waiting lists.
waiting_table = db.Table('waiting_table', db.Model.metadata,
	db.Column('classID', db.Integer, db.ForeignKey('Class.classID')),
	db.Column('delID', db.Integer, db.ForeignKey('Delegate.delID'))
)

##User
class User(db.Model):
	__tablename__ = 'User'
	userID = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	username = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))
	type = db.Column(db.String(100))

	__mapper_args__ = {
		'polymorphic_identity': 'base',
		'polymorphic_on': type
	}

	#This property should return True if the user is authenticated, i.e. they have provided valid credentials.
	def is_authenticated(self):
		return True

	#This property should return True if this is an active user.
	def is_active(self):
		return True

	#This property should return True if this is an anonymous user. (Actual users should return False instead.)
	def is_anonymous(self):
		return False

	#This method must return a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback.
	def get_id(self):
		return self.userID

##Admin
class Admin(User):
	__tablename__ = 'Admin'
	adminID = db.Column(db.Integer, db.ForeignKey('User.userID'), primary_key = True)

	__mapper_args__ = {
		'polymorphic_identity': 'Admin',
	}

##Trainer
class Trainer(User):
	__tablename__ = 'Trainer'
	trainerID = db.Column(db.Integer,db.ForeignKey('User.userID'), primary_key = True)
	address = db.Column(db.String(100))
	phone = db.Column(db.Integer)


	__mapper_args__ = {
		'polymorphic_identity': 'Trainer',
	}

##Delegates
class Delegate(User):
	__tablename__ = 'Delegate'
	delID = db.Column(db.Integer, db.ForeignKey('User.userID'), primary_key = True)
	classList= db.relationship("Class", secondary = association_table)

	__mapper_args__ = {
		'polymorphic_identity': 'Delegate',
	}

##Room
class Room(db.Model):
	__tablename__ = 'Room'
	roomID = db.Column(db.Integer, primary_key = True)
	capacity = db.Column(db.Integer)
	roomType = db.Column(db.String(100))
	roomCode = db.Column(db.String(100))
	building = db.Column(db.String(100))
	location = db.Column(db.String(100))
	facilities = db.Column(db.String(100))
	picURL = db.Column(db.String(100))
	accessRating = db.Column(db.String(100))

##Class
class Class(db.Model):
	__tablename__ = 'Class'
	classID = db.Column(db.Integer, primary_key = True)
	coursePoint = db.Column(db.Integer, db.ForeignKey('Course.courseID'))
	course = db.relationship("Course", foreign_keys = [coursePoint])
	courseID = db.Column(db.Integer)
	title = db.Column(db.String(100))
	description = db.Column(db.String(100))
	capacity = db.Column(db.Integer)
	#Temporarily set the default to the time now for ease of testing.
	startTime = db.Column(db.DateTime, default = datetime.utcnow )
	#Set the default 60 need to discuss the unit of time.
	duration = db.Column(db.Integer, default = 60)
	#Both the follow fields default to None unless specified.
	reqFac = db.Column(db.String(100), default = 'None')
	preTrain = db.Column(db.String(100), default = 'None')
	locationPoint = db.Column(db.Integer, db.ForeignKey('Room.roomID'))
	location = db.relationship("Room", foreign_keys = [locationPoint])
	trainerPoint = db.Column(db.Integer, db.ForeignKey('Trainer.trainerID'))
	trainer = db.relationship("Trainer", foreign_keys = [trainerPoint])
	attendanceList = db.relationship('Delegate', secondary = association_table)
	waitList = db.relationship('Delegate', secondary = waiting_table)

##courses
class Course(db.Model):
	__tablename__ = 'Course'
	courseID = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100))
	description = db.Column(db.String(100))
