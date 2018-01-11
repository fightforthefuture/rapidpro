web: librato-launch gunicorn --statsd-host=127.0.0.1:8142 temba.wsgi:application --log-file -
worker: celery -A temba worker --beat -Q flows,msgs,handler,celery -c 4