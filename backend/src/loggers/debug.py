import logging
from pathlib import Path


LOGGER_PATH = Path(__file__).parent.parent.resolve() / "logs" / "debugs.log"


logger = logging.getLogger("Exeption_logger")


logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    "%(asctime)s\t%(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


file_handler = logging.FileHandler(LOGGER_PATH)

file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
