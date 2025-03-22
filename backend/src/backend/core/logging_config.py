import logging

log_format = (
    "      %(levelname)s   [%(filename)s:%(lineno)d] {%(funcName)s} - %(message)s"
)


logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    force=True,
)

fastapi_logger = logging.getLogger("uvicorn")
access_logger = logging.getLogger("uvicorn.access")
error_logger = logging.getLogger("uvicorn.error")
fastapi_logger.setLevel(logging.DEBUG)
fastapi_logger.propagate = False


def get_logger(name: str):
    return logging.getLogger(name)
