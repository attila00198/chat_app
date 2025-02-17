import logging
import os


def setup_logging(name: str, log_file: str = "chat_server.log") -> logging.Logger:
    """
    Sets up logging for the given logger name, logging to both console and file.

    Args:
        name: The name of the logger
        log_file: Path to the log file (default: "app.log")

    Returns:
        logging.Logger: Configured logger instance

    Raises:
        OSError: If log file directory is not writable
    """
    # Ellenőrizzük, hogy a logger már létezik-e
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Ellenőrizzük, hogy a log könyvtár létezik-e és írható-e
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError as e:
            raise OSError(f"Failed to create log directory: {e}")

    try:
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Ellenőrizzük, hogy nincsenek-e már handlerek
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger

    except Exception as e:
        # Fallback logger konzolra, ha valami hiba történt
        fallback_logger = logging.getLogger(f"{name}_fallback")
        fallback_logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fallback_logger.addHandler(console)

        fallback_logger.error("Failed to setup main logger: %s", e)
        return fallback_logger
