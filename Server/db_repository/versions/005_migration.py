from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Room = Table('Room', post_meta,
    Column('roomID', Integer, primary_key=True, nullable=False),
    Column('capacity', Integer),
    Column('roomType', String(length=100)),
    Column('roomCode', String(length=100)),
    Column('building', String(length=100)),
    Column('location', String(length=100)),
    Column('facilities', String(length=100)),
    Column('picURL', String(length=100)),
    Column('accessRating', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Room'].columns['facilities'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Room'].columns['facilities'].drop()
