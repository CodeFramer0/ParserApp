import logging
import os
from datetime import timedelta
from pathlib import Path

from aiogram import Bot
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
BOT_TOKEN = env.str("BOT_TOKEN")
DUMP_CHAT_ID = env.str("DUMP_CHAT_ID")
bot = Bot(token=BOT_TOKEN)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "nopriz.apps.NoprizConfig",
    "nostroy.apps.NostroyConfig",
    "web_interface.apps.WebInterfaceConfig",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rangefilter",
    "API",
    "django_celery_beat",
    "django_celery_results",
    "django_filters",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_SECURE = False  # True для HTTPS
CSRF_COOKIE_SECURE = False  # True для HTTPS
SESSION_COOKIE_SAMESITE = "Lax"  # Или 'None'


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


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Asia/Yekaterinburg"

USE_I18N = True

USE_TZ = True

CELERY_TIMEZONE = "Asia/Yekaterinburg"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_RESULT_SERIALIZER = "json"


# Новая настройка для Celery 6.0 и выше
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BEAT_SCHEDULE = {
    "НОПРИЗ-Физ Парсинг типа работ": {
        "task": "nopriz.tasks.fiz_parse_type_of_work",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ-Физ Парсинг статуса работника": {
        "task": "nopriz.tasks.fiz_parse_status_worker",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ-Физ Парсинг основных линков": {
        "task": "nopriz.tasks.fiz_parse_main_data",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ-Физ Валидация идентификационного номера": {
        "task": "nopriz.tasks.fiz_verify_id_number",
        "schedule": timedelta(hours=12),
    },
    "НОПРИЗ-Физ Верификация основных данных": {
        "task": "nopriz.tasks.fiz_verify_parsed_data",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ-Физ Генерация excel файла": {
        "task": "nopriz.tasks.generate_excel_nopriz_fiz",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ-Юр Генерация excel файла": {
        "task": "nopriz.tasks.generate_excel_nopriz_yr",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ-Юр Парсинг данных": {
        "task": "nopriz.tasks.yr_parse_data",
        "schedule": timedelta(hours=1),
    },
    "НОПРИЗ Отправка дампа в ТГ": {
        "task": "nopriz.tasks.dumpdata_and_send_to_telegram",
        "schedule": timedelta(hours=24),
    },
}

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}
