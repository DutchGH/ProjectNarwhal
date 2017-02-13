from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
friendList = Table('friendList', pre_meta,
    Column('friends', INTEGER),
)

friendList = Table('friendList', post_meta,
    Column('Relationships', Integer),
)

postList = Table('postList', pre_meta,
    Column('posts', INTEGER),
)

postList = Table('postList', post_meta,
    Column('Posts', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['friendList'].columns['friends'].drop()
    post_meta.tables['friendList'].columns['Relationships'].create()
    pre_meta.tables['postList'].columns['posts'].drop()
    post_meta.tables['postList'].columns['Posts'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['friendList'].columns['friends'].create()
    post_meta.tables['friendList'].columns['Relationships'].drop()
    pre_meta.tables['postList'].columns['posts'].create()
    post_meta.tables['postList'].columns['Posts'].drop()
