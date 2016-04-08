from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from utils import *

default_keyboard = [
    ['[Мой профиль]'],
    ['[Инвентарь]', '[Магазин]'],
    ['[Скрыть]']
]


def start(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    user = getUser(user_id)

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
                    text=getProfile(user_id=user_id))


def inventory(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=str(getInventory(update.message.from_user.id)))


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
        msg = 'Вы перешли в комнату {} ({})'.format(getRoom(r[1]).title, r[1])
        changeRoom(user_id, r[1])
    else:
        msg = 'Используйте /room [комната]'
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=msg)


def info(bot, update):
    user_id = update.message.from_user.id
    r = str(update.message.text).split(' ')

    # Checking second argument (user ID)
    if len(r) == 2 and r[1].isdigit():
        msg = getProfile(user_id=r[1])
    elif len(r) == 2:
        msg = getProfile(user_name=r[1])
    else:
        msg = getProfile(user_id=user_id)
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

    current_user = getUser(user_id)

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
        item = getItem(inv.business, True)
        money = getUser(inv.user_id).money

        updateUser(inv.user_id, {'money': money + item.value})
        logger.info("Money added to user {}".format(inv.user_id))

        bot.sendMessage(inv.user_id, "Вам было начислено {}$ за ваш бизнес".format(item.value))
