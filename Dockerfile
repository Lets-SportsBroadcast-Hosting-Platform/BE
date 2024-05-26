FROM --platform=linux/amd64 python:3.11.9-slim as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt


WORKDIR /usr/src/app
COPY ./app /usr/src/app

EXPOSE 80
CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "80"]
