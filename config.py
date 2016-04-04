import logging
from models import session

TOKEN = 'XXXXXXXXXXXXXXXXXXXX'

HELP_TEXT = ['/me - Информация о вас',
             '/menu - Открыть меню']

logging.basicConfig(
    format='[%(asctime)s][%(name)s][%(levelname)s] - %(message)s',
    level=logging.INFO,
    # filename='bot.log'
)
logger = logging.getLogger(__name__)
db = session
