from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Posts = Table('Posts', post_meta,
    Column('postID', Integer, primary_key=True, nullable=False),
    Column('content', String(length=1000)),
    Column('date', String(length=100)),
    Column('user_ID', Integer),
    Column('user_ID2', Integer),
    Column('secure', Boolean),
    Column('rank', Float),
    Column('ratings', Float),
)

Relationships = Table('Relationships', post_meta,
    Column('relID', Integer, primary_key=True, nullable=False),
    Column('user_ID', Integer),
    Column('user_ID2', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Posts'].columns['user_ID2'].create()
    post_meta.tables['Relationships'].columns['user_ID2'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Posts'].columns['user_ID2'].drop()
    post_meta.tables['Relationships'].columns['user_ID2'].drop()
