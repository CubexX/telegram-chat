from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from models import User, Item, Room, db, Inventory
from config import logger, HELP_TEXT

default_keyboard = [
    ['[Мой профиль]'],
    ['[Инвентарь]', '[Магазин]'],
    ['[Скрыть]']
]


def start(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    user = User(user_id=user_id).get()

    # Creating menu keyboard
    reply_markup = ReplyKeyboardMarkup(default_keyboard)

    if user:
        msg = 'С возвращением, %s\nПомощь - /help' % user_name
    else:
        db.add(User(user_id, user_name))
        db.commit()
        logger.info('User {}({}) added bot'.format(user_name, user_id))

        msg = 'Добро пожаловать в ChatRoo!\nПомощь - /help'

    bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)


def help(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='\n'.join(HELP_TEXT))


def menu(bot, update):
    reply_markup = ReplyKeyboardMarkup(default_keyboard)
    bot.sendMessage(chat_id=update.message.chat_id, text='Меню открыто', reply_markup=reply_markup)


def profile(bot, update):
    user_id = update.message.from_user.id

    bot.sendMessage(update.message.chat_id,
                    text=User(user_id=user_id).profile())


def inventory(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=str(Inventory(user_id=update.message.from_user.id).get()))


def shop(bot, update):  # TODO
    pass


def hide(bot, update):
    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Меню скрыто. /menu чтобы открыть", reply_markup=reply_markup)


def room(bot, update):
    user_id = update.message.from_user.id
    r = str(update.message.text).split(' ')

    if len(r) == 2 and r[1].isdigit():
        msg = 'Вы перешли в комнату {} ({})'.format(Room(r[1]).get().title, r[1])
        Room(r[1]).change(user_id)
    else:
        msg = 'Используйте /room [комната]'
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=msg)


def info(bot, update):
    user_id = update.message.from_user.id
    r = str(update.message.text).split(' ')

    # Checking second argument (user ID)
    if len(r) == 2 and r[1].isdigit():
        msg = User(user_id=r[1]).profile()
    elif len(r) == 2:
        msg = User(user_name=r[1]).profile()
    else:
        msg = User(user_id=user_id).profile()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=msg)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def msg(bot, update):
    text = update.message.text

    if text == "[Мой профиль]":
        profile(bot, update)
    elif text == "[Инвентарь]":
        inventory(bot, update)
    elif text == "[Магазин]":
        pass
    elif text == "[Скрыть]":
        hide(bot, update)
    else:
        echo(bot, update)


def echo(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username

    current_user = User(user_id=user_id).get()

    q = db.query(User).filter(User.user_id != user_id, User.current_room == current_user.current_room).all()

    for user in q:
        now = datetime.strftime(update.message.date, "%H:%M:%S")

        message = "@%s, [%s]\n%s" % (user_name, now, update.message.text)
        bot.sendMessage(user.user_id,
                        text=message)


def error(update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def test(bot, update):
    # For debugging
    bot.sendMessage(update.message.chat_id,
                    text=str(update.message.from_user))


def business_pay(bot):
    q = db.query(Inventory).filter(Inventory.business != None).all()

    for inv in q:
        item = Item(inv.business).get(model=True)
        money = User(user_id=inv.user_id).get()

        User(user_id=inv.user_id).update({'money': money + item.value})
        logger.info("Money added to user {}".format(inv.user_id))

        bot.sendMessage(inv.user_id, "Вам было начислено {}$ за ваш бизнес".format(item.value))
