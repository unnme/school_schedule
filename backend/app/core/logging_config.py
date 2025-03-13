import logging

from rich import pretty
from rich.logging import RichHandler

# Улучшенный вывод ошибок в консоли
pretty.install()

# Создаём кастомный формат логов
log_format = "%(filename)s:%(lineno)d - %(levelname)s - %(message)s"

# Создаём обработчик RichHandler с кастомным форматированием
rich_handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=True)

# Устанавливаем формат логов
formatter = logging.Formatter(log_format)
rich_handler.setFormatter(formatter)

# Очищаем старые хендлеры
logging.root.handlers.clear()

# Настраиваем `logging` с новым обработчиком
logging.basicConfig(
    level=logging.INFO,
    handlers=[rich_handler],
    force=True,
)

# Настройка логов SQLAlchemy
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.handlers.clear()
sqlalchemy_logger.addHandler(rich_handler)
sqlalchemy_logger.setLevel(logging.INFO)
sqlalchemy_logger.propagate = False


def get_logger(name: str):
    return logging.getLogger(name)
