FROM python:latest

ENV PYTHONUNVUFFERED=1

WORKDIR /code

COPY ./code/requirements.txt /code/

RUN pip install -r requirements.txt