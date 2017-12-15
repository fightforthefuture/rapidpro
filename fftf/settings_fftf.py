from __future__ import absolute_import, unicode_literals

# -----------------------------------------------------------------------------------
# RapidPro settings file, this should allow you to deploy RapidPro to Heroku
#
# The following are requirements:
#     - `heroku stack:set heroku-16`
#     - `heroku config:set BUILD_WITH_GEO_LIBRARIES=1`
#     - a PostgresQL database at DATABASE_URL
#     - a redis instance at REDIS_URL
#
# -----------------------------------------------------------------------------------

import copy
import os

# set these before importing common settings
SECRET_KEY = os.environ.get('SECRET_KEY')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

from temba.settings_common import *  # noqa

DEBUG = False
DEBUG_TOOLBAR = False

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

# -----------------------------------------------------------------------------------
# Add a custom brand
# -----------------------------------------------------------------------------------

custom = copy.deepcopy(BRANDING['rapidpro.io'])
custom['name'] = 'RapidPro'
custom['slug'] = 'fftf'
custom['org'] = 'Fight for the Future'
custom['api_link'] = 'http://fightforthefuture.org'
custom['domain'] = 'fightforthefuture.org'
custom['email'] = 'team@fightforthefuture.org'
custom['support_email'] = 'team@fightforthefuture.org'
custom['allow_signups'] = True
BRANDING['custom-brand.io'] = custom

# -----------------------------------------------------------------------------------
# Message Broker Configuration
# -----------------------------------------------------------------------------------
HOSTNAME = os.environ.get('APPLICATION_HOSTNAME')
ALLOWED_HOSTS = ['*']

MAGE_API_URL = os.environ.get('MAGE_API_URL')
MAGE_AUTH_TOKEN = os.environ.get('MAGE_API_TOKEN')  # should be same token as configured on Mage side

# -----------------------------------------------------------------------------------
# Database Configuration
# -----------------------------------------------------------------------------------

import dj_database_url
_default_database_config = dj_database_url.config(conn_max_age=500)
_default_database_config['ATOMIC_REQUESTS'] = True

# Heroku standard databases include PostGIS
_default_database_config['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

_direct_database_config = _default_database_config.copy()
_default_database_config['DISABLE_SERVER_SIDE_CURSORS'] = True

DATABASES = {
    'default': _default_database_config,
    'direct': _direct_database_config
}

# -----------------------------------------------------------------------------------
# Redis & Cache Configuration
# -----------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# -----------------------------------------------------------------------------------
# RapidPro configuration settings
# -----------------------------------------------------------------------------------

SEND_MESSAGES = True
SEND_WEBHOOKS = True
SEND_EMAILS = True

######
# Unused features
SEND_AIRTIME = False
SEND_CHATBASE = False
SEND_CALLS = False

INTERNAL_IPS = ('127.0.0.1',)
