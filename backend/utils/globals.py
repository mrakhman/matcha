import logging
import os


logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
logger.info(f"LOG LEVEL: {logger.level}")
logger.debug("Logger initialized")
