from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
friendList = Table('friendList', post_meta,
    Column('friends', Integer),
)

postList = Table('postList', post_meta,
    Column('posts', Integer),
)

Relationships = Table('Relationships', pre_meta,
    Column('relID', INTEGER, primary_key=True, nullable=False),
    Column('user_ID', INTEGER),
    Column('user_ID2', INTEGER),
)

Relationships = Table('Relationships', post_meta,
    Column('relID', Integer, primary_key=True, nullable=False),
    Column('target', Integer),
)

Posts = Table('Posts', pre_meta,
    Column('postID', INTEGER, primary_key=True, nullable=False),
    Column('content', VARCHAR(length=1000)),
    Column('date', VARCHAR(length=100)),
    Column('secure', BOOLEAN),
    Column('user_ID', INTEGER),
    Column('rank', FLOAT),
    Column('ratings', FLOAT),
    Column('user_ID2', INTEGER),
)

Posts = Table('Posts', post_meta,
    Column('postID', Integer, primary_key=True, nullable=False),
    Column('content', String(length=1000)),
    Column('date', String(length=100)),
    Column('target', Integer),
    Column('secure', Boolean),
    Column('rank', Float),
    Column('ratings', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['friendList'].create()
    post_meta.tables['postList'].create()
    pre_meta.tables['Relationships'].columns['user_ID'].drop()
    pre_meta.tables['Relationships'].columns['user_ID2'].drop()
    post_meta.tables['Relationships'].columns['target'].create()
    pre_meta.tables['Posts'].columns['user_ID'].drop()
    pre_meta.tables['Posts'].columns['user_ID2'].drop()
    post_meta.tables['Posts'].columns['target'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['friendList'].drop()
    post_meta.tables['postList'].drop()
    pre_meta.tables['Relationships'].columns['user_ID'].create()
    pre_meta.tables['Relationships'].columns['user_ID2'].create()
    post_meta.tables['Relationships'].columns['target'].drop()
    pre_meta.tables['Posts'].columns['user_ID'].create()
    pre_meta.tables['Posts'].columns['user_ID2'].create()
    post_meta.tables['Posts'].columns['target'].drop()
