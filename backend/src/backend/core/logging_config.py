import logging

log_format = "%(levelname)s:     [%(filename)s:%(lineno)d] {%(funcName)s} - %(message)s"


logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    force=True,
)

sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.WARNING)
sqlalchemy_logger.propagate = True


def get_logger(name: str):
    return logging.getLogger(name)
