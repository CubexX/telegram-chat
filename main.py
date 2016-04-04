from telegram.ext import Updater
from config import *
import handlers


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # job_queue = updater.job_queue
    # job_queue.put(sendNewVideo, CHECK_INTERVAL, repeat=True)

    dp.addTelegramCommandHandler("test", handlers.test)

    dp.addTelegramCommandHandler("start", handlers.start)
    dp.addTelegramCommandHandler("help", handlers.help)
    dp.addTelegramCommandHandler("me", handlers.profile)
    dp.addTelegramCommandHandler('menu', handlers.menu)

    dp.addTelegramMessageHandler(handlers.msg)

    # dp.addTelegramMessageHandler(handlers.echo)
    dp.addErrorHandler(handlers.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
