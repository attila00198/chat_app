import logging

def setup_logging(name):
    """
    Sets up logging for the given logger name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%y-%m-%d %H:%M")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
