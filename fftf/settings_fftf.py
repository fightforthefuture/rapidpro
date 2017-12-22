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

IS_PROD = True
DEBUG = False
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}
INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat', 'crispy_forms',)

# -----------------------------------------------------------------------------------
# Add a custom brand, make it the default
# -----------------------------------------------------------------------------------

custom = copy.deepcopy(BRANDING['rapidpro.io'])
custom['name'] = 'RapidPro'
custom['slug'] = 'fftf'
custom['org'] = 'Fight for the Future'
custom['domain'] = os.environ.get('APPLICATION_HOSTNAME')
custom['link'] = 'https://%s' % os.environ.get('APPLICATION_HOSTNAME')
custom['email'] = 'team@fightforthefuture.org'
custom['support_email'] = 'team@fightforthefuture.org'
custom['allow_signups'] = False
custom['host'] = os.environ.get('APPLICATION_HOSTNAME')
custom['description'] = "Visually build activism messaging applications with open source software."
custom['splash'] = ['brands/fftf/splash.jpg',]
custom['styles'] = ['brands/fftf/font/style.css',]
BRANDING['fftf'] = custom
DEFAULT_BRAND = 'fftf'

# -----------------------------------------------------------------------------------
# Heroku filesystem is ephemeral, use S3 via boto
# -----------------------------------------------------------------------------------

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'fftf.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'fftf.storage_backends.PrivateMediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

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
COMPRESS_STORAGE = 'fftf.storage_backends.CachedStaticStorage'
COMPRESS_OFFLINE_CONTEXT = []
for brand in BRANDING.values():
    if HOSTNAME == 'localhost' or 'staging' in HOSTNAME or brand.get('host', None) == HOSTNAME:
        context = dict(STATIC_URL=STATIC_URL, base_template='frame.html', debug=False, testing=False)
        context['brand'] = dict(slug=brand['slug'], styles=brand['styles'])
        COMPRESS_OFFLINE_CONTEXT.append(context)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
) + MIDDLEWARE_CLASSES

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

MAGE_AUTH_TOKEN = os.environ.get('MAGE_AUTH_TOKEN', 'missing_rapidpro_token')

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

BROKER_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = os.environ.get('REDIS_URL')

# -----------------------------------------------------------------------------------
# Email Configuration
# -----------------------------------------------------------------------------------
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'admin@fightforthefuture.org'

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
