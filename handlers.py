from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from config import *
from models import User, Room

default_keyboard = [
    ['[Мой профиль]'],
    ['[Инвентарь]', '[Магазин]'],
    ['[Скрыть]']
]


def start(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    user = db.query(User).filter(User.user_id == user_id).all()

    reply_markup = ReplyKeyboardMarkup(default_keyboard)

    if len(user) == 1:
        msg = 'С возвращением, %s\nПомощь - /help' % user_name
    else:
        db.add(User(user_id, user_name))
        db.commit()
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
    _user = db.query(User, Room).filter(User.user_id == user_id, User.current_room == Room.id).all()[0]
    room = _user[1]
    user = _user[0]

    msg = 'Ник: @%s\nID: %s\nКомната: %s (%s)\nДеньги: %s$' % (user.user_name,
                                                               user_id,
                                                               room.title,
                                                               user.current_room,
                                                               user.money)
    bot.sendMessage(update.message.chat_id,
                    text=msg)


def inventory(bot, update):  # TODO
    pass


def shop(bot, update):  # TODO
    pass


def hide(bot, update):
    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Меню скрыто. /menu чтобы открыть", reply_markup=reply_markup)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def msg(bot, update):
    text = update.message.text

    if text == "[Мой профиль]":
        profile(bot, update)
    elif text == "[Инвентарь]":
        pass
    elif text == "[Магазин]":
        pass
    elif text == "[Скрыть]":
        hide(bot, update)
    else:
        echo(bot, update)


def echo(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username

    current_user = db.query(User).filter(User.user_id == user_id).all()[0]

    q = db.query(User).filter(User.user_id != user_id, User.current_room == current_user.current_room).all()

    for user in q:
        now = datetime.strftime(update.message.date, "%H:%M:%S")

        message = "@%s, [%s]\n%s" % (user_name, now, update.message.text)
        bot.sendMessage(user.user_id,
                        text=message)


def error(update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def test(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text=str(update.message.from_user))