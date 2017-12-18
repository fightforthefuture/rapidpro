from __future__ import absolute_import, unicode_literals

# -----------------------------------------------------------------------------------
# RapidPro settings file, this should allow you to deploy RapidPro to Heroku
#
# The following are requirements:
#     - `heroku stack:set heroku-16`
#     - `heroku config:set BUILD_WITH_GEO_LIBRARIES=1`
#     - `heroku config:set DISABLE_COLLECTSTATIC=1`
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

DEBUG = True
DEBUG_TOOLBAR = True

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}
INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat', 'crispy_forms',)

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
custom['allow_signups'] = False
custom['host'] = os.environ.get('APPLICATION_HOSTNAME')
BRANDING['fftf'] = custom

# -----------------------------------------------------------------------------------
# Static files compression and hosting
# -----------------------------------------------------------------------------------

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc --include-path="%s" {infile} {outfile}' % os.path.join(PROJECT_DIR, '../static', 'less')),
    ('text/coffeescript', 'coffee --compile --stdio')
)
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_OFFLINE_CONTEXT = []
for brand in BRANDING.values():
    if HOSTNAME == 'localhost' or 'staging' in HOSTNAME or brand.get('host', None) == HOSTNAME:
        context = dict(STATIC_URL=STATIC_URL, base_template='frame.html', debug=False, testing=False)
        context['brand'] = dict(slug=brand['slug'], styles=brand['styles'])
        COMPRESS_OFFLINE_CONTEXT.append(context)

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
] + list(MIDDLEWARE_CLASSES)

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

HOSTNAME = os.environ.get('APPLICATION_HOSTNAME')
ALLOWED_HOSTS = ['*']
