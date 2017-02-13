from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Room = Table('Room', post_meta,
    Column('roomID', Integer, primary_key=True, nullable=False),
    Column('capacity', Integer),
    Column('roomType', String(length=100)),
    Column('picURL', String(length=100)),
    Column('accessRating', String(length=100)),
    Column('location', String(length=100)),
)

Trainer = Table('Trainer', post_meta,
    Column('trainerID', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('phone', Integer),
    Column('email', String(length=100)),
    Column('username', String(length=100)),
    Column('password', String(length=100)),
)

Class = Table('Class', post_meta,
    Column('classID', Integer, primary_key=True, nullable=False),
    Column('courseID', Integer),
    Column('title', String(length=100)),
    Column('description', String(length=100)),
    Column('capacity', Integer),
    Column('startTime', DateTime),
    Column('duration', Integer),
    Column('requiredFacilities', String(length=100)),
    Column('prerequsitTraining', String(length=100)),
    Column('locationPoint', Integer),
    Column('trainerPoint', Integer),
    Column('waitListPoint', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Room'].columns['picURL'].create()
    post_meta.tables['Trainer'].columns['email'].create()
    post_meta.tables['Trainer'].columns['phone'].create()
    post_meta.tables['Class'].columns['courseID'].create()
    post_meta.tables['Class'].columns['waitListPoint'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Room'].columns['picURL'].drop()
    post_meta.tables['Trainer'].columns['email'].drop()
    post_meta.tables['Trainer'].columns['phone'].drop()
    post_meta.tables['Class'].columns['courseID'].drop()
    post_meta.tables['Class'].columns['waitListPoint'].drop()
