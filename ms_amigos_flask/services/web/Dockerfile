# pull official base image
FROM python:3.8.1-slim-buster
EXPOSE 5000

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV FLASK_APP project/__init__.py
ENV FLASK_ENV development
ENV DATABASE_URL postgresql://postgres:postgres@sapamigosdb:5432/amigos
ENV SQL_HOST sapamigosdb
ENV SQL_PORT 5432
ENV DATABASE postgres
ENV APP_FOLDER /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD ["python", "/usr/src/app/manage.py", "run", "-h", "0.0.0.0"]
