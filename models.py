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
    hp = Column('hp', Integer, default=100)
    current_room = Column('current_room', ForeignKey('rooms.id'), default=ROOM_DEFAULT_ID)
    money = Column('money', Integer, default=DEFAULT_MONEY)

    def __init__(self, user_id, user_name, hp, current_room=ROOM_DEFAULT_ID, money=DEFAULT_MONEY):
        self.user_id = user_id
        self.user_name = user_name
        self.hp = hp
        self.current_room = current_room
        self.money = money

    def __repr__(self):
        return "<User('{}','{}','{}','{}','{}')>".format(self.user_id,
                                                         self.user_name,
                                                         self.hp,
                                                         self.current_room,
                                                         self.money)


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
        return "<Room('{}','{}','{}')>".format(self.title,
                                               self.owner,
                                               self.password)


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.user_id'))

    gun = Column('gun', ForeignKey('items.id'))
    armor = Column('armor', ForeignKey('items.id'))
    house = Column('house', ForeignKey('items.id'))
    clothes = Column('clothes', ForeignKey('items.id'))
    business = Column('business', ForeignKey('items.id'))
    animal = Column('animal', ForeignKey('items.id'))

    gun_value = Column('gun_value', Integer)
    armor_value = Column('armor_value', Integer)
    house_value = Column('house_value', Integer)
    clothes_value = Column('clothes_value', Integer)
    business_value = Column('business_value', Integer)
    animal_value = Column('animal_value', Integer)

    def __init__(self, id, user_id, gun, armor, house, clothes, business, animal, gun_value=None, armor_value=None,
                 house_value=None, clothes_value=None, business_value=None, animal_value=None):
        self.id = id
        self.user_id = user_id
        self.gun = gun
        self.armor = armor
        self.house = house
        self.clothes = clothes
        self.business = business
        self.animal = animal

        self.gun_value = gun_value
        self.armor_value = armor_value
        self.house_value = house_value
        self.clothes_value = clothes_value
        self.business_value = business_value
        self.animal_value = animal_value

    def __repr__(self):
        return "<Inventory('{}','{}','{}','{}','{}','{}','{}','{}')" \
               "('{}','{}','{}','{}','{}','{}')>".format(self.id,
                                                         self.user_id,
                                                         self.gun,
                                                         self.armor,
                                                         self.house,
                                                         self.clothes,
                                                         self.business,
                                                         self.animal,
                                                         self.gun_value,
                                                         self.armor_value,
                                                         self.house_value,
                                                         self.clothes_value,
                                                         self.business_value,
                                                         self.animal_value
                                                         )


class Item(Base):
    __tablename__ = 'items'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    cost = Column('cost', String)
    type = Column('type', String)
    value = Column('value', Integer)

    def __init__(self, id, title, cost, type, value):
        self.id = id
        self.title = title
        self.cost = cost
        self.type = type
        self.value = value

    def __repr__(self):
        return "<Item('{}','{}','{}','{}','{}')>".format(self.id,
                                                         self.title,
                                                         self.cost,
                                                         self.type,
                                                         self.value)


engine = create_engine(DATABASE, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
