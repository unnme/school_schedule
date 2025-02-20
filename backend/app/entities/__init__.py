from importlib import import_module

from app.core.settings import settings


for app_dir in settings.base.ENTITIES_DIR.iterdir():
    if app_dir.is_dir() and not app_dir.name.startswith("__"):
        models_file = app_dir / "models.py"
        if models_file.exists():
            module_name = f"app.entities.{app_dir.name}.models"
            import_module(module_name)
