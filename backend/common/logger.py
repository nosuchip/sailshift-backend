import logging

from backend import config

logger = logging.getLogger(config.APP_NAME)

logger.setLevel(logging.DEBUG)
