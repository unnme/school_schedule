import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.core.config import settings
from app.core.depends import get_user_manager
from app.entities.user.models import User


bearer_transport = BearerTransport(tokenUrl=settings.api_prefix.bearer_token_url)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.security.SECRET_KEY,
        lifetime_seconds=3600,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend]) 
current_active_user = fastapi_users.current_user(active=True)
