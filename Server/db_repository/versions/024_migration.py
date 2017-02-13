from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Trainer = Table('Trainer', post_meta,
    Column('trainerID', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('address', String(length=100)),
    Column('phone', Integer),
    Column('email', String(length=100)),
    Column('username', String(length=100)),
    Column('password', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Trainer'].columns['address'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Trainer'].columns['address'].drop()
