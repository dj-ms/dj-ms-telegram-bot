"""
Django settings for dj_ms_core project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import os
import sys
from pathlib import Path

import dj_database_url
import dotenv
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load env variables from *.env* file
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-9uq@=l5ykga+r$2=+nk+abwy)ej-y2n%!-u^fe^0=ybj)*+)d!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DJANGO_DEBUG') == 'False' else True

# Use different app label for each microservice. For example, 'product' for product microservice
APP_LABEL = os.getenv('DJ_MS_APP_LABEL', '')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]

extra_allowed_hosts = os.getenv('DJANGO_ALLOWED_HOSTS', None)

if extra_allowed_hosts:
    assert isinstance(extra_allowed_hosts.split(','), list)
    ALLOWED_HOSTS.extend(extra_allowed_hosts.split(','))

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = (
    'http://127.0.0.1:8000',
    'http://localhost:8000',
)

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

extra_csrf_trusted_origins = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', None)

if extra_csrf_trusted_origins:
    assert isinstance(extra_csrf_trusted_origins.split(','), list)
    CSRF_TRUSTED_ORIGINS.extend(extra_csrf_trusted_origins.split(','))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'whitenoise.runserver_nostatic',
    'corsheaders',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
    'auditlog',
    'python_telegram_bot_django_persistence',

    # microservice apps
    'authentication',
    'ms_auth_router',
    'app',

    # django_cleanup cleanup files after deleting model instance with FileField or ImageField fields
    'django_cleanup.apps.CleanupConfig'
]

MIDDLEWARE = [
    'core.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_ROUTERS = [
    'ms_auth_router.routers.DefaultRouter',
]

ROUTE_APP_LABELS = ('authentication', )

AUTH_DB = 'default'

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3', conn_max_age=600)
}

if auth_db := os.getenv('AUTH_DB_URL'):
    AUTH_DB = 'auth_db'
    DATABASES['auth_db'] = dj_database_url.parse(auth_db)

AUTH_USER_MODEL = 'authentication.User'

# -----> Rest Framework
REST_AUTH_TOKEN_MODEL = 'authentication.Token'

REST_AUTH_TOKEN_TTL = os.getenv('DJANGO_REST_AUTH_TOKEN_TTL', 60 * 60 * 24)

REST_AUTH_TOKEN_CREATOR = 'authentication.utils.create_token'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'authentication.utils.ExpiringTokenAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.api.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = os.getenv('DJANGO_LANGUAGE_CODE', 'en-us')

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uz', _('Uzbek')),
)

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True

DATE_FORMAT = 'Y.m.d'

DATETIME_FORMAT = 'Y.m.d H:i'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'assets'
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----> RABBITMQ
BROKER_URL = os.getenv('BROKER_URL', 'amqp://guest:guest@localhost:5672')


# -----> CELERY
CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'


# -----> SENTRY
if SENTRY_DSN := os.getenv('SENTRY_DSN', None):

    SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT', 'development')
    environment = f'{APP_LABEL}-{SENTRY_ENVIRONMENT}' if APP_LABEL else SENTRY_ENVIRONMENT

    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(), CeleryIntegration()
        ],

        debug=DEBUG,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,

        environment=environment
    )


# -----> TELEGRAM
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    logging.error(
        "Please provide TELEGRAM_TOKEN in .env file.\n"
        "Example of .env file: https://github.com/ohld/django-telegram-bot/blob/main/.env_example"
    )
    sys.exit(1)
