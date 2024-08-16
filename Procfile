release: python src/django/manage.py tailwind build 
web: gunicorn app.wsgi:application --chdir 'src/django'