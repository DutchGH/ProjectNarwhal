from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
property = Table('property', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('address', VARCHAR(length=500)),
    Column('start_date', DATETIME),
    Column('duration', INTEGER),
    Column('rent', FLOAT),
)

task = Table('task', pre_meta,
    Column('desc', VARCHAR(length=100), primary_key=True, nullable=False),
    Column('done', BOOLEAN),
    Column('date', VARCHAR(length=100)),
    Column('details', VARCHAR(length=100)),
)

accounts = Table('accounts', post_meta,
    Column('accID', String(length=100), primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('login', String(length=100)),
    Column('password', String(length=100)),
    Column('pic', String(length=100)),
    Column('rank', Integer),
)

posts = Table('posts', post_meta,
    Column('postID', String(length=100), primary_key=True, nullable=False),
    Column('content', String(length=100)),
    Column('date', String(length=100)),
    Column('poster', String(length=100)),
    Column('target', String(length=100)),
    Column('secure', Boolean),
)

relationships = Table('relationships', post_meta,
    Column('userOne', String(length=100), primary_key=True, nullable=False),
    Column('userTwo', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['property'].drop()
    pre_meta.tables['task'].drop()
    post_meta.tables['accounts'].create()
    post_meta.tables['posts'].create()
    post_meta.tables['relationships'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['property'].create()
    pre_meta.tables['task'].create()
    post_meta.tables['accounts'].drop()
    post_meta.tables['posts'].drop()
    post_meta.tables['relationships'].drop()
