FROM --platform=linux/amd64 python:3.11.9-slim as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG SERVER_SECRET_KEY
ARG KAKAO_CLIENT_ID
ARG KAKAO_RESTAPI_KEY
ARG NAVER_CLIENT_ID
ARG NAVER_SECRET_KEY
ARG DATABASE_HOST
ARG DATABASE_USER
ARG DATABASE_PWD
ARG DATABASE_NAME
ARG BUSSINESS_SERVICE_KEY
ARG AWS_ACCESS_KEY_ID_
ARG AWS_SECRET_ACCESS_KEY_
ARG REGION_NAME
ARG BUCKET_NAME
ARG SGISAPI_KEY
ARG SGISAPI_SECRET

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# .env 파일 생성
RUN echo "SERVER_SECRET_KEY=${SERVER_SECRET_KEY}" >> /code/app/.env && \
    echo "KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID}" >> /code/app/.env && \
    echo "KAKAO_RESTAPI_KEY=${KAKAO_RESTAPI_KEY}" >> /code/app/.env && \
    echo "NAVER_CLIENT_ID=${NAVER_CLIENT_ID}" >> /code/app/.env && \
    echo "NAVER_SECRET_KEY=${NAVER_SECRET_KEY}" >> /code/app/.env && \
    echo "DATABASE_HOST=${DATABASE_HOST}" >> /code/app/.env && \
    echo "DATABASE_USER=${DATABASE_USER}" >> /code/app/.env && \
    echo "DATABASE_PWD=${DATABASE_PWD}" >> /code/app/.env && \
    echo "DATABASE_NAME=${DATABASE_NAME}" >> /code/app/.env && \
    echo "BUSSINESS_SERVICE_KEY=${BUSSINESS_SERVICE_KEY}" >> /code/app/.env && \
    echo "AWS_ACCESS_KEY_ID_=${AWS_ACCESS_KEY_ID_}" >> /code/app/.env && \
    echo "AWS_SECRET_ACCESS_KEY_=${AWS_SECRET_ACCESS_KEY_}" >> /code/app/.env && \
    echo "REGION_NAME=${REGION_NAME}" >> /code/app/.env && \
    echo "BUCKET_NAME=${BUCKET_NAME}" >> /code/app/.env && \
    echo "SGISAPI_KEY=${SGISAPI_KEY}" >> /code/app/.env && \
    echo "SGISAPI_SECRET=${SGISAPI_SECRET}" >> /code/app/.env

WORKDIR /usr/src/app
COPY ./app /usr/src/app

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
