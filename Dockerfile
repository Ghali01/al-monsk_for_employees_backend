FROM python:3.9-alpine

RUN apk add --no-cache gcc musl-dev python3-dev

RUN pip install ruamel.yaml.clib 
COPY  . ./ 


RUN pip install -r r.txt


# RUN python manage.py migrate 
# CMD python manage.py migrate 
# && python manage.py runserver 0.0.0.0:8000
# CMD ['gunicorn' ,'interviews.wsgi:application', '--bind'' 0.0.0.0:8000']
CMD python manage.py migrate && uvicorn staff_server.asgi:application --host 0.0.0.0