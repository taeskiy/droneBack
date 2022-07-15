FROM python:3.9.4

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app
CMD python manage.py migrate && python manage.py collectstatic --no-input && gunicorn -b 0.0.0.0:8000 --log-level info --reload -w 4 DroneDelivery.wsgi:application
