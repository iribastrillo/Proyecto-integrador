worker: sh -c "python src/django/manage.py migrate && python src/django/manage.py createsuperuser --noinput"
web: gunicorn app.wsgi:application --chdir 'src/django'