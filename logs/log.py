import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
def log_debug(message):
    logging.debug(message)

def log_message(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message, error):
    logging.error(message)
    logging.exception(error)