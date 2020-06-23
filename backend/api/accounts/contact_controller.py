from backend import config
from backend.common import mailer
from backend.common.logger import logger


def send_contact_us(email, subject, message):
    try:
        mailer.send_raw(email, tuple(config.EMAIL_CONTACT_US_ADDRESS), subject, message)

        return True
    except Exception as ex:
        logger.exception(f'Unable to send contact us message')
        logger.exception(ex)

        return False
