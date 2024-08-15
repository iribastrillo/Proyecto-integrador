worker: sh -c "python src/django/manage.py tailwind install"
web: gunicorn app.wsgi:application --chdir 'src/django'