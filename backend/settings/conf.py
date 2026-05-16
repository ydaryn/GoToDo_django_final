from os import environ

ENV_ID_POSSIBLE_OPTIONS = ["local", "prod"]
GOTODO_ENV_ID = environ.get("GOTODO_ENV_ID", "local")
SECRET_KEY = environ.get(
    "SECRET_KEY",
    "django-insecure-(^_^gfp3**yddhcs%6q!gm@%3#6mp3nwmxr(15df$ypky$ckgv",
)
