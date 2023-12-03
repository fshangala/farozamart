source env/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py loaddata yaml