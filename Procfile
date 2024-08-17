release: python src/django/manage.py migrate
web: gunicorn app.wsgi:application --chdir 'src/django'