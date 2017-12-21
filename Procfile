web: bin/link_bins; gunicorn temba.wsgi:application --log-file -
worker: celery worker --beat -Q flows,msgs,handler,celery -c 2