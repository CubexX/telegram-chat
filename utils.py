from config import *
from models import User, Inventory, Item


def getUser(user_id):
    cached = cache.get('user_%s' % user_id)
    if cached:
        logger.info('Sent from cache user_%s' % user_id)
        return cached
    else:
        q = db.query(User).filter(User.user_id == user_id).all()[0]
        cache.set('user_%s' % user_id, q)
        logger.info('Added to cache user_%s' % user_id)
        return q


def getInventory(user_id):
    inv = db.query(Inventory).filter(Inventory.user_id == user_id).all()[0]
    gun = getItem(inv.gun)
    armor = getItem(inv.armor)
    house = getItem(inv.house)
    clothes = getItem(inv.clothes)
    business = getItem(inv.business)
    animal = getItem(inv.animal)

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


def getItem(id):
    cached = cache.get('item_%s' % id)
    if cached:
        logger.info('Sent from cache item_%s' % id)
        return '{0} ({1})'.format(cached[0].title, cached[0].value)
    else:
        q = db.query(Item).filter(Item.id == id).all()
        if q:
            cache.set('item_%s' % id, q)
            logger.info('Added to cache item_%s' % id)
            return '{0} ({1})'.format(q[0].title, q[0].value)
        else:
            return "Нет"
