from __future__ import absolute_import, unicode_literals

# -----------------------------------------------------------------------------------
# Sample RapidPro settings file, this should allow you to deploy RapidPro locally on
# a PostgreSQL database.
#
# The following are requirements:
#     - a postgreSQL database named 'temba', with a user name 'temba' and
#       password 'temba' (with postgis extensions installed)
#     - a redis instance listening on localhost
# -----------------------------------------------------------------------------------

import warnings
import copy

SECRET_KEY = 'asdf this is a bad secret key'

from .settings_fftf import *  # noqa

IS_PROD = False
DEBUG = True
DEBUG_TOOLBAR = True

HOSTNAME = 'fftf.ngrok.io'
ALLOWED_HOSTS = ['*']

# allow signups on dev
BRANDING['fftf']['allow_signups'] = True

# -----------------------------------------------------------------------------------
# Database Configuration(we expect a Postgres instance on localhost)
# -----------------------------------------------------------------------------------
_default_database_config = {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'temba',
    'USER': 'temba',
    'PASSWORD': 'temba',
    'HOST': 'localhost',
    'PORT': '',
    'ATOMIC_REQUESTS': True,
    'CONN_MAX_AGE': 60,
    'OPTIONS': {}
}
_direct_database_config = _default_database_config.copy()
_default_database_config['DISABLE_SERVER_SIDE_CURSORS'] = True

DATABASES = {
    'default': _default_database_config,
    'direct': _direct_database_config
}

# -----------------------------------------------------------------------------------
# Redis & Cache Configuration (we expect a Redis instance on localhost)
# -----------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/%s" % (REDIS_HOST, REDIS_PORT, REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

INTERNAL_IPS = ('127.0.0.1',)

# -----------------------------------------------------------------------------------
# Load development apps
# -----------------------------------------------------------------------------------
INSTALLED_APPS = INSTALLED_APPS + ('storages', )
if DEBUG_TOOLBAR:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar', )

# -----------------------------------------------------------------------------------
# In development, add in extra logging for exceptions and the debug toolbar
# -----------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = ('temba.middleware.ExceptionMiddleware',) + MIDDLEWARE_CLASSES
if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES

# -----------------------------------------------------------------------------------
# In development, perform background tasks in the web thread (synchronously)
# -----------------------------------------------------------------------------------
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = 'memory'

# -----------------------------------------------------------------------------------
# This setting throws an exception if a naive datetime is used anywhere. (they should
# always contain a timezone)
# -----------------------------------------------------------------------------------
warnings.filterwarnings('error', r"DateTimeField .* received a naive datetime",
                        RuntimeWarning, r'django\.db\.models\.fields')

# -----------------------------------------------------------------------------------
# Reset static file compression and storage on development
# -----------------------------------------------------------------------------------
STATIC_URL = '/sitestatic/'
MEDIA_URL = '/media/'

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_DEBUG_TOGGLE = 'debug_compress'

DEFAULT_FILE_STORAGE = 'fftf.storage_backends.SiteStaticStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE 
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_OFFLINE_CONTEXT = []
