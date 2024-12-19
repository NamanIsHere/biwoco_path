"""
Logging utility module.
This module provides logging functions for debugging, informational messages, warnings, and errors.
"""
import logging

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
def log_debug(message):
    """
    Logs a debug-level message.

    :param message: The message to log.
    """
    logging.debug(message)

def log_message(message):
    """
    Logs an info-level message.

    :param message: The message to log.
    """
    logging.info(message)

def log_warning(message):
    """
    Logs a warning-level message.

    :param message: The message to log.
    """
    logging.warning(message)

def log_error(message, error):
    """
    Logs an error-level message and an exception traceback.

    :param message: The error message to log.
    :param error: The exception object to log.
    """
    logging.error(message)
    logging.exception(error)
