import logging

def setup_logging(name, log_file="app.log"):
    """
    Sets up logging for the given logger name, logging to both console and file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Stream handler (optional: to still show logs in console)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%y-%m-%d %H:%M")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

