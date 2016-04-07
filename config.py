import logging
from models import session
import memcache

cache = memcache.Client(['127.0.0.1:11211'], debug=1)

TOKEN = ''
BUSINESS_PAY_INTERVAL = 60 * 60

HELP_TEXT = ['/me - Информация о вас',
             '/menu - Открыть меню',
             '/inventory - Инвентарь',
             '/room [комната] - Смена комнаты',
             '/info [пользователь] - Профиль пользователя']

logging.basicConfig(
    format='[%(asctime)s][%(name)s][%(levelname)s] - %(message)s',
    level=logging.INFO,
    # filename='bot.log'
)
logger = logging.getLogger(__name__)
db = session
