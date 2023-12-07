FROM python:3.10
RUN git clone https://github.com/fshangala/farozamart.git
WORKDIR /farozamart
RUN pip install -r requirements.txt
RUN cp .env-production .env
RUN python manage.py migrate
RUN python manage.py createsuperuser --no-input
RUN python manage.py loaddata data
RUN python manage.py loaddata store

CMD ["python","manage.py","runserver","0.0.0.0:80"]
