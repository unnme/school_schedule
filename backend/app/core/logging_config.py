import logging

from rich import pretty
from rich.logging import RichHandler

pretty.install()

# Создаём RichHandler для красивого вывода
rich_handler = RichHandler(rich_tracebacks=True, show_time=False)

# Очищаем root-логгер перед настройкой (ВАЖНО!)
logging.root.handlers.clear()

# Настраиваем общий логгер
logging.basicConfig(
    level=logging.NOTSET,
    handlers=[rich_handler],
)

# Настройка SQLAlchemy логов
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")

# Очищаем все старые обработчики у SQLAlchemy (исправление проблемы дублирования)
sqlalchemy_logger.handlers.clear()

# Добавляем только RichHandler
sqlalchemy_logger.addHandler(rich_handler)

# Устанавливаем уровень логирования (можно изменить на DEBUG, если надо)
sqlalchemy_logger.setLevel(logging.INFO)

# Полностью отключаем пропагирование, чтобы логи SQLAlchemy не дублировались в root-логгер
sqlalchemy_logger.propagate = False

logger = logging.getLogger(__name__)
