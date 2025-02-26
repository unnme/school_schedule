import logging

from rich import pretty
from rich.logging import RichHandler

pretty.install()

rich_handler = RichHandler(rich_tracebacks=True, show_time=False)

logging.root.handlers.clear()

logging.basicConfig(
    level=logging.NOTSET,
    handlers=[rich_handler],
    force=True,
)

# Настройка логов SQLAlchemy
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.handlers.clear()
sqlalchemy_logger.addHandler(rich_handler)
sqlalchemy_logger.setLevel(logging.INFO)
sqlalchemy_logger.propagate = False
