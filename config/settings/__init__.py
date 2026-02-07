import os

environment = os.getenv("DJANGO_ENV", "local").lower()

if environment == "prod":
	from .prod import *  # noqa: F403
elif environment == "base":
	from .base import *  # noqa: F403
else:
	from .local import *  # noqa: F403