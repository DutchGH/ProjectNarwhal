from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Posts = Table('Posts', pre_meta,
    Column('postID', INTEGER, primary_key=True, nullable=False),
    Column('content', VARCHAR(length=1000)),
    Column('date', VARCHAR(length=100)),
    Column('secure', BOOLEAN),
    Column('poster', INTEGER),
    Column('target', INTEGER),
)

Posts = Table('Posts', post_meta,
    Column('postID', Integer, primary_key=True, nullable=False),
    Column('content', String(length=1000)),
    Column('date', String(length=100)),
    Column('user_ID', Integer),
    Column('secure', Boolean),
)

Relationships = Table('Relationships', pre_meta,
    Column('relID', INTEGER, primary_key=True, nullable=False),
    Column('userOne', INTEGER),
    Column('userTwo', INTEGER),
)

Relationships = Table('Relationships', post_meta,
    Column('relID', Integer, primary_key=True, nullable=False),
    Column('user_ID', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Posts'].columns['poster'].drop()
    pre_meta.tables['Posts'].columns['target'].drop()
    post_meta.tables['Posts'].columns['user_ID'].create()
    pre_meta.tables['Relationships'].columns['userOne'].drop()
    pre_meta.tables['Relationships'].columns['userTwo'].drop()
    post_meta.tables['Relationships'].columns['user_ID'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Posts'].columns['poster'].create()
    pre_meta.tables['Posts'].columns['target'].create()
    post_meta.tables['Posts'].columns['user_ID'].drop()
    pre_meta.tables['Relationships'].columns['userOne'].create()
    pre_meta.tables['Relationships'].columns['userTwo'].create()
    post_meta.tables['Relationships'].columns['user_ID'].drop()
