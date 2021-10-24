FROM python:3.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# copy project
COPY ./requirements.txt /requirements.txt
COPY ./app /app

# install dependencies and create a user    
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    pip install -r /requirements.txt && \
    apk del .tmp-build-deps && \
    adduser -D user

# setup default user
USER user