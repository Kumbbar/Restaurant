try:
    from apps.users.models import User
except ImportError:
    raise ImportError(
        "Couldn't import User model from app"
    )

from core_settings.settings import DEBUG