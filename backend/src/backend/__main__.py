import uvicorn

from backend import app
from backend.core.logging_config import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
