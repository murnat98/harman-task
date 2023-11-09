import logging
import sys

LOG_RECORD_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)-20s | %(message)s"
DATE_FORMAT = "%d/%m/%Y %I:%M:%S %p"


def init_logger(logging_level: str):
    simple_log_formatter = logging.Formatter(LOG_RECORD_FORMAT, datefmt=DATE_FORMAT)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(simple_log_formatter)
    logging.basicConfig(
        handlers=[stdout_handler],
        level=logging_level,
    )
