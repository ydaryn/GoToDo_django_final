import os

from settings.conf import GOTODO_ENV_ID, ENV_ID_POSSIBLE_OPTIONS
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from apps.notifications.routing import websocket_urlpatterns
from apps.notifications.auth import JWTAuthMiddleware




assert GOTODO_ENV_ID in ENV_ID_POSSIBLE_OPTIONS, (
    f"Set correct GOTODO_ENV_ID env var. Possible options: {ENV_ID_POSSIBLE_OPTIONS}"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{GOTODO_ENV_ID}")



django_asgi_app= get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )  
        )
    }
)