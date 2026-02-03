import logging
from pathlib import Path

def setup_logger(log_path: str):
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()])

    logging.info("Logger initialized")
