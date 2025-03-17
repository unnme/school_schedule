from fastapi_users.authentication import AuthenticationBackend, BearerTransport

from src.api.depends.authentication.strategy import get_database_strategy
from src.core.config import settings

SECRET = settings.security.SECRET_KEY
bearer_transport = BearerTransport(tokenUrl=settings.api_config.bearer_token_url)

auth_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
