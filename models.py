from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from config import cache, logger
from re import sub

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

    def __init__(self, user_id=None, user_name=None, hp=None, current_room=ROOM_DEFAULT_ID, money=DEFAULT_MONEY):
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

    def get(self):
        cached = cache.get('user_%s' % self.user_id)
        if cached:
            logger.info('Sent from cache user_%s' % self.user_id)
            return cached
        else:
            q = db.query(User).filter(User.user_id == self.user_id).all()[0]
            cache.set('user_%s' % self.user_id, q)
            logger.info('Added to cache user_%s' % self.user_id)
            return q

    def update(self, update):
        user = db.query(User).filter(User.user_id == self.user_id)
        user.update(update)
        db.commit()
        cache.set('user_%s' % self.user_id, user.all()[0])
        logger.info('Cache updated user_%s' % self.user_id)

    def profile(self):
        if self.user_name:
            self.user_name = sub('@', '', self.user_name)
            query = db.query(User, Room).filter(User.user_name == self.user_name, User.current_room == Room.id).all()[0]
            logger.info('Sent from database user_%s' % self.user_name)
        else:
            query = db.query(User, Room).filter(User.user_id == self.user_id, User.current_room == Room.id).all()[0]
            logger.info('Sent from database user_%s' % self.user_id)

        room = query[1]
        user = query[0]

        msg = 'Ник: @{}\n' \
              'HP: {}\n' \
              'ID: {}\n' \
              'Комната: {} ({})\n' \
              'Деньги: {}$\n\n' \
              'Инвентарь - /inventory'.format(user.user_name,
                                              user.hp,
                                              user.user_id,
                                              room.title,
                                              user.current_room,
                                              user.money)
        return msg


class Room(Base):
    __tablename__ = 'rooms'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    owner = Column('owner', ForeignKey('users.id'), default=ROOM_OWNER_DEFAULT_ID)
    password = Column('password', String, default=None)

    def __init__(self, id=None, title=None, owner=ROOM_OWNER_DEFAULT_ID, password=None):
        self.id = id
        self.title = title
        self.owner = owner
        self.password = password

    def __repr__(self):
        return "<Room('{}','{}','{}','{}')>".format(self.id,
                                                    self.title,
                                                    self.owner,
                                                    self.password)

    def get(self):
        cached = cache.get('room_%s' % self.id)
        if cached:
            logger.info('Sent from cache room_%s' % self.id)
            return cached[0]
        else:
            q = db.query(Room).filter(Room.id == self.id).all()
            cache.set('room_%s' % self.id, q)
            logger.info('Added to cache room_%s' % self.id)
            return q[0]

    def change(self, user_id):
        r = db.query(Room).filter(Room.id == self.id).all()
        if r:
            User(user_id=user_id).update({'current_room': self.id})


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

    def __init__(self, id=None, user_id=None, gun=None, armor=None, house=None,
                 clothes=None, business=None, animal=None, gun_value=None, armor_value=None,
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

    def get(self):
        inv = db.query(Inventory).filter(Inventory.user_id == self.user_id).all()[0]
        gun = Item(inv.gun).get()
        armor = Item(inv.armor).get()
        house = Item(inv.house).get()
        clothes = Item(inv.clothes).get()
        business = Item(inv.business).get()
        animal = Item(inv.animal).get()

        msg = 'Оружие - {}\n' \
              'Броня - {}\n' \
              'Дом - {}\n' \
              'Одежда - {}\n' \
              'Бизнес - {}\n' \
              'Питомец - {}'.format(gun,
                                    armor,
                                    house,
                                    clothes,
                                    business,
                                    animal)
        return msg


class Item(Base):
    __tablename__ = 'items'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    cost = Column('cost', String)
    type = Column('type', String)
    value = Column('value', Integer)

    def __init__(self, id=None, title=None, cost=None, type=None, value=None):
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

    def get(self, model=None):
        cached = cache.get('item_%s' % self.id)
        res = None

        if cached:
            logger.info('Sent from cache item_%s' % self.id)
            res = '{0} ({1})'.format(cached[0].title, cached[0].value)
            if model:
                res = cached[0]
        else:
            q = db.query(Item).filter(Item.id == self.id).all()
            if q:
                cache.set('item_%s' % self.id, q)
                logger.info('Added to cache item_%s' % self.id)
                res = '{0} ({1})'.format(q[0].title, q[0].value)
                if model:
                    res = q[0]
            else:
                res = 'Нет'

        return res


engine = create_engine(DATABASE, echo=False, connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
db = session
