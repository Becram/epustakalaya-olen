"""
Django settings for pustakalaya project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from pkg_resources import resource_filename

# config.json contains the keys that need to overwrite in base.py
config_file = resource_filename("config", "config.json")

# Pull configuration detail from config/config.json file
with open(config_file) as configuration:
    config = json.load(configuration)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'pustakalaya_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*=up=#to)&a6g@v0jjx%9kj4ema&wr5g4yw44fagd#*e1l0^7v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # dependent third party apps
    'jet',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRDPARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.google',
    'crispy_forms',
    'star_ratings',

]

PUSTAKALAYA_APPS = [
    'pustakalaya_apps.core',
    'pustakalaya_apps.document',
    'pustakalaya_apps.collection',
    'pustakalaya_apps.audio',
    'pustakalaya_apps.video',
    'pustakalaya_apps.image',
    'pustakalaya_apps.other',
    'pustakalaya_apps.dashboard',
    'pustakalaya_apps.pustakalaya_search',
    'pustakalaya_apps.pustakalaya_account',


]
INSTALLED_APPS += THIRDPARTY_APPS + PUSTAKALAYA_APPS

# Enable development apps in debug mode


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'pustakalaya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'pustakalaya.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# Don't put static root in version control
try:
    STATIC_ROOT = config["STATIC_ROOT"]
except KeyError:
    ImproperlyConfigured("{} improperly configured".format("MEDIA_ROOT"))
# Per application basic
# static_dist files are dispatched automatically by webpack by reading static_src directory.
STATICFILES_DIRS = (
    ('static'),
)

# Media Configuration
MEDIA_URL = '/media/'
try:
    MEDIA_ROOT = config["MEDIA_ROOT"]
except KeyError:
    ImproperlyConfigured("{} improperly configured".format("MEDIA_ROOT"))

# Elastic search settings.
ES_HOST = os.environ.get('ES_HOST', '127.0.0.1')

ES_INDEX = os.environ.get('ES_INDEX', 'pustakalaya')
# Override ES_INDEX
ES_INDEX = 'pustakalaya'

ES_INDEX_SETTINGS = {
    'number_of_shards': os.getenv("ES_NUMBER_OF_SHARDS", 1),
    'number_of_replicas': os.getenv("ES_NUMBER_OF_REPLICAS", 0),
}

ES_CONNECTIONS = {
    'default': {
        'hosts': [{
            'host': ES_HOST,
            'index': ES_INDEX,
            **ES_INDEX_SETTINGS,
            'verify_certs': False,
            'use_ssl': os.environ.get('ES_USE_SSL', False) == 'True',
            'port': os.environ.get('ES_PORT', '9200'),
            'timeout': 10
        }]
    }
}

## Cache server configuration.
try:
    REDIS_IP = config["REDIS"]["IP"]
    REDIS_PORT = config["REDIS"]["PORT"]

except KeyError:
    raise ImproperlyConfigured("{} or {} Improperly configured in config.json".format("REDIS IP", "REDIS_PORT"))

# Cache time to live is 0 minutes.
CACHE_TTL = 60 * 0  # 0 minutes
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/1".format(REDIS_IP, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "pustakalaya"
    }
}

# Django jet configuration
JET_DEFAULT_THEME = 'default'
JET_SIDE_MENU_COMPACT = True

## Translation settings.
LANGUAGES = (
    ('en', _('English')),
    ('ne', _('Nepali')),
)

# Translation local path
LOCALE_PATHS = (
    os.path.join(os.path.dirname(BASE_DIR), 'locale'),
)

# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# smtp settings
try:
    EMAIL_HOST = config["EMAIL"]["EMAIL_HOST"]
    EMAIL_PORT = config["EMAIL"]["EMAIL_PORT"]
    EMAIL_HOST_USER = config["EMAIL"]["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = config["EMAIL"]["EMAIL_HOST_PASSWORD"]
    EMAIL_USE_TLS = bool(config["EMAIL"]["EMAIL_USE_TLS"])
    FEEDBACK_MESSAGE_TO = config["EMAIL"]["FEEDBACK_MESSAGE_TO"]
    ADMINS = config["EMAIL"]["ADMIN_EMAILS"]
except KeyError:
    raise ImproperlyConfigured("{}".format("Email settings"))

## Django allauth configuration
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Redirect to dashboard when login is successfull.
# Configuration of django all auth
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_FORM_CLASS = "pustakalaya_apps.pustakalaya_account.forms.SignupForm"
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Crispy forms settings.
CRISPY_TEMPLATE_PACK = 'bootstrap4'

## Django logging settings
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'logs')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'null': {
#             'level':'DEBUG',
#             'class':'django.utils.log.NullHandler',
#         },
#         'console':{
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         'logfile': {
#             'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(LOG_DIR, 'pustakalaya.log'),
#             'maxBytes': 1024*1024*5, # 5MB
#             'backupCount': 0,
#             'formatter': 'verbose',
#         },
#     },
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s',
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s|%(message)s'
#         },
#     },
#     'loggers': {
#         'myapp.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'myapp.tasks': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'myapp.management': {
#             'handlers': ['console', 'logfile'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'myapp.models': {
#             'handlers': ['console', 'logfile'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     }
# }
