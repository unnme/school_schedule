import uuid

from fastapi_users import FastAPIUsers

from app.entities.auth.models import User
from app.api.depends.authentication.user_manager import get_user_manager
from app.api.depends.authentication.backend import auth_backend


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
