"""
This module provides a Logger class that sets up a shared logger object for logging messages across the entire application.

The Logger class allows modules to easily log messages by providing a pre-configured logger object. It sets up the logging configuration, including the logging level, format, and handlers to write to a shared log file and console.

Usage:
    To use the Logger class, create an instance of it in your module and call the `get_logger()` method to retrieve the configured logger object. You can then use the logger object to log messages at different levels (e.g., debug, info, warning, error).

Example:
    # Import the Logger class
    from utils.log_config import Logger

    # Create an instance of the Logger class for your module
    logger = Logger(__name__).get_logger()

    # Log a debug message
    logger.debug("This is a debug message")

    # Log an error message
    logger.error("An error occurred")

Note:
    - The shared log file is stored in the 'logs' directory relative to the module's location.
    - The log file name includes the current date and time to ensure uniqueness.
    - The log messages are written to both the log file and the console.

"""

import logging
import os
from datetime import datetime

# Initialize a variable to hold the common log filename
log_filename = None


class Logger:
    """
    The Logger class is responsible for setting up a shared logger object for logging messages across the entire application.
    """

    def __init__(self, module_name):
        """
        Initializes a new instance of the Logger class for a given module.

        Args:
            module_name (str): The name of the module using this logger.
        """
        global log_filename
        self.module_name = module_name
        self.logger = logging.getLogger(module_name)
        if log_filename is None:
            log_filename = self._setup_log_filename()
        self._set_up()

    def _setup_log_filename(self):
        """
        Sets up the shared log filename for the first time when the logger is initialized.

        Returns:
            str: The log file name with the current date and time.
        """
        if not os.path.exists("logs"):
            os.makedirs("logs")
        return f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    def _set_up(self):
        """
        Sets up the logging configuration for this logger instance.
        This function configures the logging level, format, and handlers to write to a shared log file and console.
        """
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(log_filename),
                    logging.StreamHandler(),  # To also output to console
                ],
            )

    def get_logger(self):
        """
        Returns the configured logger object.

        Returns:
            logging.Logger: The configured logger object.
        """
        return self.logger
