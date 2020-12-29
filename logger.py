## LOGGING UTILS

import logging
from config import global_config
from logging.handlers import RotatingFileHandler

cfg = global_config.global_config.get_instance().CFG

MAX_BYTES = 10000000 # Maximum size for a log file
BACKUP_COUNT = 15 # Maximum number of old log files

def setup_custom_logger(name):
    logger = logging.getLogger(name) 
    logger.setLevel(logging.INFO) # the level should be the lowest level set in handlers

    log_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    info_handler = RotatingFileHandler(cfg['log_path'] + 'info.log', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    info_handler.setFormatter(log_format)
    info_handler.setLevel(logging.INFO)
    logger.addHandler(info_handler)

    error_handler = RotatingFileHandler(cfg['log_path'] + 'error.log', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    error_handler.setFormatter(log_format)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    return logger
