# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
COPY . /code/
WORKDIR /code/
RUN python -m pip install --upgrade pip
RUN pip install -r /code/requirements.txt