import os
from datetime import timedelta
from settings.conf import *  # noqa: F403

# ==========================================
# Paths
# ==========================================
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR  = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

ROOT_URLCONF       = "settings.urls"
WSGI_APPLICATION   = "settings.wsgi.application"
ASGI_APPLICATION   = "settings.asgi.application"
AUTH_USER_MODEL    = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_AND_THIRD_PARTY_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "parler",
    "adrf",
    "drf_spectacular",
    "channels"
]

PROJECT_APPS = [
    "apps.accounts",
    "apps.projects",  
    "apps.agile",    
]

INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,  # noqa: F405
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
"""
Languages
"""
SUPPORTED_LANGUAGES = ["en","ru","kk"]
LANGUAGES = [
    ("en","English"),
    ("ru","Русский"),
    ("kk","Қазақша"),
]

"""
parler instructions
"""
PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "ru"},
        {"code": "kk"},
    ),
    "default": {
        "fallback": "en",
        "hide_untranslated": False,
    },
}


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"



LANGUAGE_CODE = "en"
LOCALE_PATHS = [os.path.join(BASE_DIR,"locale")]
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# API Documentation (Swagger / Spectacular)

SPECTACULAR_SETTINGS = {
    'TITLE': 'GoToDo API',
    'DESCRIPTION': 'Документация бэкенда для таск-менеджера GoToDo (KBTU Final Project)',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    # Настройка, чтобы прямо в Swagger можно было нажать кнопку Authorize и вставить JWT-токен
    'SECURITY': [{'BearerAuth': []}],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Введите токен в формате: Bearer <ваш_access_token>'
            }
        }
    }
}