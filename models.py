from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

ROOM_DEFAULT_ID = 1
ROOM_OWNER_DEFAULT_ID = 1
DEFAULT_MONEY = 100
DATABASE = 'sqlite:///bot.db'


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    user_name = Column('user_name', String)
    current_room = Column('current_room', ForeignKey('rooms.id'), default=ROOM_DEFAULT_ID)
    money = Column('money', Integer, default=DEFAULT_MONEY)

    def __init__(self, user_id, user_name, current_room=ROOM_DEFAULT_ID, money=DEFAULT_MONEY):
        self.user_id = user_id
        self.user_name = user_name
        self.current_room = current_room
        self.money = money

    def __repr__(self):
        return "<User('%s','%s','%s','%s')>" % (self.user_id, self.user_name, self.current_room, self.money)


class Room(Base):
    __tablename__ = 'rooms'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    owner = Column('owner', ForeignKey('users.id'), default=ROOM_OWNER_DEFAULT_ID)
    password = Column('password', String, default=None)

    def __init__(self, title, owner=ROOM_OWNER_DEFAULT_ID, password=None):
        self.title = title
        self.owner = owner
        self.password = password

    def __repr__(self):
        return "<Room('%s','%s','%s')>" % (self.title, self.owner, self.password)


engine = create_engine(DATABASE, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
