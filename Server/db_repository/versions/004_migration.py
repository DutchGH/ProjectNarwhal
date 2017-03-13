from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Trainer = Table('Trainer', pre_meta,
    Column('trainerID', INTEGER, primary_key=True, nullable=False),
    Column('address', VARCHAR(length=100)),
    Column('phone', INTEGER),
    Column('email', VARCHAR(length=100)),
)

User = Table('User', post_meta,
    Column('userID', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('username', String(length=100)),
    Column('email', String(length=100)),
    Column('password', String(length=100)),
    Column('type', String(length=100)),
)

Room = Table('Room', post_meta,
    Column('roomID', Integer, primary_key=True, nullable=False),
    Column('capacity', Integer),
    Column('roomType', String(length=100)),
    Column('roomCode', String(length=100)),
    Column('building', String(length=100)),
    Column('location', String(length=100)),
    Column('picURL', String(length=100)),
    Column('accessRating', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Trainer'].columns['email'].drop()
    post_meta.tables['User'].columns['email'].create()
    post_meta.tables['Room'].columns['building'].create()
    post_meta.tables['Room'].columns['roomCode'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Trainer'].columns['email'].create()
    post_meta.tables['User'].columns['email'].drop()
    post_meta.tables['Room'].columns['building'].drop()
    post_meta.tables['Room'].columns['roomCode'].drop()
