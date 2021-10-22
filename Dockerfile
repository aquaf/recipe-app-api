FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app

# Make venv and install dependencies and add user
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    adduser -D user

USER user