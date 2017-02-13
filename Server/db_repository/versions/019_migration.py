from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Accounts = Table('Accounts', post_meta,
    Column('accID', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('login', String(length=100)),
    Column('password', String(length=100)),
    Column('desc', String(length=100)),
    Column('pic', String(length=100)),
    Column('rank', Float),
    Column('ratings', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Accounts'].columns['desc'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Accounts'].columns['desc'].drop()
