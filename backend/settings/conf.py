#Third party modules

from decouple import config
from os import environ

ENV_ID_POSSIBLE_OPTIONS = ["local", "prod"]

GOTODO_ENV_ID = config("GOTODO_ENV_ID", cast=str)

SECRET_KEY = 'django-insecure-(^_^gfp3**yddhcs%6q!gm@%3#6mp3nwmxr(15df$ypky$ckgv'
