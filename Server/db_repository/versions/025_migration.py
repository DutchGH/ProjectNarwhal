from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Class = Table('Class', pre_meta,
    Column('classID', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=100)),
    Column('description', VARCHAR(length=100)),
    Column('capacity', INTEGER),
    Column('startTime', DATETIME),
    Column('duration', INTEGER),
    Column('requiredFacilities', VARCHAR(length=100)),
    Column('prerequsitTraining', VARCHAR(length=100)),
    Column('locationPoint', INTEGER),
    Column('trainerPoint', INTEGER),
    Column('courseID', INTEGER),
    Column('waitListPoint', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Class'].columns['waitListPoint'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Class'].columns['waitListPoint'].create()
