import os
import sys
from pathlib import Path
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    DEBUG = False
    ENABLE_S3 = True
else:
    DEBUG = True
    ENABLE_S3 = False

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'server/apps'))
sys.path.append(os.path.join(BASE_DIR, 'server/util'))
sys.path.append(os.path.join(BASE_DIR, 'server/vendor'))

ENABLE_CACHE = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
	'jadedgamer.com', 'www.jadedgamer.com',
	'jadedgamer.herokuapp.com', #Heroku
    '8po2lakic6.execute-api.us-east-1.amazonaws.com', #AWS
]

ADMINS = (('Tyler Rilling', 'tyler@jadedgamer.com'))
MANAGERS = ADMINS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#Cache
if ENABLE_CACHE:
    import urlparse
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
                'OPTIONS': {
                    'PASSWORD': redis_url.password,
                    'DB': 0,
            }
        },
        "staticfiles": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "TIMEOUT": 60 * 60 * 24 * 365,
            "LOCATION": "static",
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


# ====================
# = #Global Settings =
# ====================

BROKER_HOST = "localhost"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = "25"
#EMAIL_USE_TLS = True
TIME_ZONE = 'US/Pacific'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
AUTH_USER_MODEL = 'coreExtend.Account'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ALLOW_NEW_REGISTRATIONS = False
WSGI_APPLICATION = 'server.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'server/static'), )

if ENABLE_S3:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = os.environ.get('LIVE_STATIC_URL', 'https://static.example.com/')
    MEDIA_URL = os.environ.get('LIVE_MEDIA_URL', 'https://static.example.com/media/')
else:
    STATICFILES_STORAGE = 'coreExtend.storage.StaticFilesStorage'
    STATIC_URL = '/static/'
    MEDIA_URL = '/static/media/'

#Site Settings
SITE_NAME = os.environ.get('SITE_NAME', 'jadedgamer.com')
SITE_DESC =  os.environ.get('SITE_DESC', 'Just another news site.')
SITE_URL =  os.environ.get('SITE_URL', '/')
SITE_AUTHOR = os.environ.get('SITE_AUTHOR', 'Tyler Rilling')

#Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '123')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '123')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', 'static.example.com')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_BUCKET_DOMAIN', 'static.example.com')
AWS_S3_SECURE_URLS = True

#from boto.s3.connection import OrdinaryCallingFormat
#AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

REST_FRAMEWORK = {
    'PAGINATE_BY': 25, # Default to 25
    'PAGINATE_BY_PARAM': 'page_size', # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100, # Maximum limit allowed when using `?page_size=xxx`.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# ===========================
# = Django-specific Modules =
# ===========================

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = os.environ.get('SECRET_KEY', '4eJUc9x86aXSLG07QgM1qZskVYZTBsWRkRMQc04rPLLgjos1wp')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'server/templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'coreExtend.context_processors.template_settings',
                'coreExtend.context_processors.template_times',
                'replica.context_processors.currentSite',
                'django.template.context_processors.request',
            ],
            'debug': DEBUG,
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'coreExtend.middleware.SubdomainURLRoutingMiddleware',
    'coreExtend.middleware.MultipleProxyMiddleware',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

ROOT_URLCONF = 'server.urls'

SUBDOMAIN_URLCONFS = {
	None: 'server.urls',
    'api': 'server.apps.api.urls',
}

#SESSION_COOKIE_DOMAIN = '.jadedgamer.com'


INSTALLED_APPS = (
    #Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    #external
    'storages',
    'rest_framework',
    'pagedown',

    #Internal
    'coreExtend',
)

LOGGING = {
    "version": 1,
    # Don't throw away default loggers.
    "disable_existing_loggers": False,
    "handlers": {
        # Redefine console logger to run in production.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        # Redefine django logger to use redefined console logging.
        "django": {
            "handlers": ["console"],
        }
    }
}
