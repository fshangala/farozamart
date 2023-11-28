FROM python:3.10
WORKDIR /app
COPY ./ .
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN cp .env-production .env
RUN python manage.py createsuperuser --no-input

CMD ["python","manage.py","runserver","0.0.0.0:80"]
