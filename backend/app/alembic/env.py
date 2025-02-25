from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Импортируйте настройки
from app.core.settings import settings
from app.core.database import Base

# Конфигурация логирования из alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Установите путь к подключению через pydantic Settings
config.set_main_option("sqlalchemy.url", settings.database.sync_db_url)

# Целевая мета информация
target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в онлайн-режиме."""
    connectable = create_engine(settings.database.sync_db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Отслеживание изменений типов
            render_as_batch=True,  # Важно для SQLite
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
