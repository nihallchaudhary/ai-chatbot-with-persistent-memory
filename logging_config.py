import logging
import sys


def setup_logging(
    log_level: str = "INFO",
):

    level = getattr(
        logging,
        log_level.upper(),
        logging.INFO,
    )

    formatter = logging.Formatter(
        (
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )

    console_handler = (
        logging.StreamHandler(
            sys.stdout
        )
    )

    console_handler.setFormatter(
        formatter
    )

    root_logger = logging.getLogger()

    root_logger.setLevel(level)

    root_logger.handlers.clear()

    root_logger.addHandler(
        console_handler
    )