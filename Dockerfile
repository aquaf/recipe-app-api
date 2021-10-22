FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app

# Make venv and install dependencies and add user
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    pip install -r /requirements.txt && \
    apk del .tmp-build-deps && \
    adduser -D user

USER user