release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn uatf_sistema.wsgi --bind 0.0.0.0:$PORT --log-file -