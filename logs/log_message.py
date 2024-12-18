import logging

logging.basicConfig(
        filename='logs/scraping.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
def log_message_to_file(message):
    logging.info(message)