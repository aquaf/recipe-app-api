FROM python:3.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

# copy requirements
COPY ./requirements.txt /requirements.txt

# install dependencies and create a user
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# setup default user
RUN mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static
RUN adduser -D user && \
    chown -R user:user /vol/ && \
    chmod -R 755 /vol/web/
USER user

# copy project
COPY . .
