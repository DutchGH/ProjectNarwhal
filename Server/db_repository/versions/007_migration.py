from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
friendship = Table('friendship', pre_meta,
    Column('accID', INTEGER),
    Column('postID', INTEGER),
    Column('relID', INTEGER),
)

Relationships = Table('Relationships', post_meta,
    Column('relID', Integer, primary_key=True, nullable=False),
    Column('userOne', Integer),
    Column('userTwo', Integer),
)

Posts = Table('Posts', post_meta,
    Column('postID', Integer, primary_key=True, nullable=False),
    Column('content', String(length=1000)),
    Column('date', String(length=100)),
    Column('poster', Integer),
    Column('target', Integer),
    Column('secure', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['friendship'].drop()
    post_meta.tables['Relationships'].columns['userOne'].create()
    post_meta.tables['Relationships'].columns['userTwo'].create()
    post_meta.tables['Posts'].columns['poster'].create()
    post_meta.tables['Posts'].columns['target'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['friendship'].create()
    post_meta.tables['Relationships'].columns['userOne'].drop()
    post_meta.tables['Relationships'].columns['userTwo'].drop()
    post_meta.tables['Posts'].columns['poster'].drop()
    post_meta.tables['Posts'].columns['target'].drop()
