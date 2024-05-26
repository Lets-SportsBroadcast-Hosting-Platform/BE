FROM --platform=linux/amd64 python:3.11.9-slim as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG SERVER_SECRET_KEY \
    KAKAO_CLIENT_ID \
    KAKAO_RESTAPI_KEY \
    NAVER_CLIENT_ID \
    NAVER_SECRET_KEY \
    DATABASE_HOST \
    DATABASE_USER \
    DATABASE_PWD \
    DATABASE_NAME \
    BUSSINESS_SERVICE_KEY \
    AWS_ACCESS_KEY_ID  \
    AWS_SECRET_ACCESS_KEY \
    REGION_NAME \
    BUCKET_NAME

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN echo "SERVER_SECRET_KEY=${SERVER_SECRET_KEY}" > /code/app/.env && \
    echo "KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID}" >> /code/app/.env && \
    echo "KAKAO_RESTAPI_KEY=${KAKAO_RESTAPI_KEY}" >> /code/app/.env && \
    echo "NAVER_CLIENT_ID=${NAVER_CLIENT_ID}" >> /code/app/.env && \
    echo "NAVER_SECRET_KEY=${NAVER_SECRET_KEY}" >> /code/app/.env && \
    echo "DATABASE_HOST=${DATABASE_HOST}" >> /code/app/.env && \
    echo "DATABASE_USER=${DATABASE_USER}" >> /code/app/.env && \
    echo "DATABASE_PWD=${DATABASE_PWD}" >> /code/app/.env && \
    echo "DATABASE_NAME=${DATABASE_NAME}" >> /code/app/.env && \
    echo "BUSSINESS_SERVICE_KEY=${BUSSINESS_SERVICE_KEY}" >> /code/app/.env && \
    echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> /code/app/.env && \
    echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> /code/app/.env && \
    echo "BUCKET_NAME=${BUCKET_NAME}" >> /code/app/.env && \
    echo "REGION_NAME=${REGION_NAME}" >> /code/app/.env

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
