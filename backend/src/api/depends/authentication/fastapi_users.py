import uuid

from fastapi_users import FastAPIUsers

from src.api.depends.authentication.backend import auth_backend
from src.api.depends.authentication.user_manager import get_user_manager
from src.entities._auth.models import User

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
