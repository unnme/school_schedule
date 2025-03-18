from importlib import import_module

from backend.core.pathes import base_pathes

for app_dir in base_pathes.entities_dir.iterdir():
    if app_dir.is_dir() and not app_dir.name.startswith("_"):
        models_file = app_dir / "models.py"
        if models_file.exists():
            module_name = f"backend.entities.{app_dir.name}.models"
            import_module(module_name)
