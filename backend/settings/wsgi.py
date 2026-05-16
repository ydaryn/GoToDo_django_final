# Python modules
import os

from django.core.wsgi import get_wsgi_application

# Project modules
from settings.conf import ENV_ID_POSSIBLE_OPTIONS, GOTODO_ENV_ID

assert (
    GOTODO_ENV_ID in ENV_ID_POSSIBLE_OPTIONS
), f"Set correct GOTODO_ENV_ID env var. Possible options: {ENV_ID_POSSIBLE_OPTIONS}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{GOTODO_ENV_ID}")

application = get_wsgi_application()
