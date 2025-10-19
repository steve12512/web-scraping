import logging
import colorlog


def get_logger():
    logger = colorlog.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        file_handler = logging.FileHandler("logging.txt", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
