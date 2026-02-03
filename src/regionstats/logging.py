import logging
from pathlib import Path

def setup_logger(log_path: str):
    """
    Configure application-wide logger.
    """
    log_file = Path(log_path)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()])

    logging.info("Logger initialized")
