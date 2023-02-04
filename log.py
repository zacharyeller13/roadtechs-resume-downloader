import logging
import os

def filter_console_logs(record: logging.LogRecord) -> bool:
    return not record.msg.startswith("Variables:")

def create_logger() -> logging.Logger:
    """Setup a `Logger` for printing to console and a log file

    :return: Logger
    """

    # Set the file for writing log output
    log_file = f"{os.path.dirname(__file__)}/log.log"

    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Setup file logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # Setup console logging
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.INFO)
    stream_handler.addFilter(filter_console_logs)

    # Create the logger and add the file and stream handlers
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger