from telegram.ext import Updater
from config import TOKEN, BUSINESS_PAY_INTERVAL
import handlers


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Business payment
    job_queue = updater.job_queue
    job_queue.put(handlers.business_pay, BUSINESS_PAY_INTERVAL, repeat=True)

    dp.addTelegramCommandHandler('test', handlers.test)

    dp.addTelegramCommandHandler('start', handlers.start)
    dp.addTelegramCommandHandler('help', handlers.help)
    dp.addTelegramCommandHandler('me', handlers.profile)
    dp.addTelegramCommandHandler('menu', handlers.menu)
    dp.addTelegramCommandHandler('inventory', handlers.inventory)
    dp.addTelegramCommandHandler('room', handlers.room)
    dp.addTelegramCommandHandler('info', handlers.info)

    dp.addTelegramMessageHandler(handlers.msg)

    dp.addErrorHandler(handlers.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
