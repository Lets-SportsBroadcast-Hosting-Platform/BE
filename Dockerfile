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
ARG MESSAGE_API_KEY
ARG MESSAGE_API_SECRET

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN pip install --no-cache-dir -r /code/requirements.txt

WORKDIR /usr/src/app
COPY ./app /usr/src/app

# 디버깅을 위해 ARG 출력
RUN echo "SERVER_SECRET_KEY=${SERVER_SECRET_KEY}" && \
    echo "KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID}" && \
    echo "KAKAO_RESTAPI_KEY=${KAKAO_RESTAPI_KEY}" && \
    echo "NAVER_CLIENT_ID=${NAVER_CLIENT_ID}" && \
    echo "NAVER_SECRET_KEY=${NAVER_SECRET_KEY}" && \
    echo "DATABASE_HOST=${DATABASE_HOST}" && \
    echo "DATABASE_USER=${DATABASE_USER}" && \
    echo "DATABASE_PWD=${DATABASE_PWD}" && \
    echo "DATABASE_NAME=${DATABASE_NAME}" && \
    echo "BUSSINESS_SERVICE_KEY=${BUSSINESS_SERVICE_KEY}" && \
    echo "AWS_ACCESS_KEY_ID_=${AWS_ACCESS_KEY_ID_}" && \
    echo "AWS_SECRET_ACCESS_KEY_=${AWS_SECRET_ACCESS_KEY_}" && \
    echo "REGION_NAME=${REGION_NAME}" && \
    echo "BUCKET_NAME=${BUCKET_NAME}" && \
    echo "SGISAPI_KEY=${SGISAPI_KEY}" && \
    echo "SGISAPI_SECRET=${SGISAPI_SECRET}" && \
    echo "MESSAGE_API_KEY=${MESSAGE_API_KEY}" && \
    echo "MESSAGE_API_SECRET=${MESSAGE_API_SECRET}"

# .env 파일 생성
RUN echo "SERVER_SECRET_KEY=${SERVER_SECRET_KEY}" >> .env && \
    echo "KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID}" >> .env && \
    echo "KAKAO_RESTAPI_KEY=${KAKAO_RESTAPI_KEY}" >> .env && \
    echo "NAVER_CLIENT_ID=${NAVER_CLIENT_ID}" >> .env && \
    echo "NAVER_SECRET_KEY=${NAVER_SECRET_KEY}" >> .env && \
    echo "DATABASE_HOST=${DATABASE_HOST}" >> .env && \
    echo "DATABASE_USER=${DATABASE_USER}" >> .env && \
    echo "DATABASE_PWD=${DATABASE_PWD}" >> .env && \
    echo "DATABASE_NAME=${DATABASE_NAME}" >> .env && \
    echo "BUSSINESS_SERVICE_KEY=${BUSSINESS_SERVICE_KEY}" >> .env && \
    echo "AWS_ACCESS_KEY_ID_=${AWS_ACCESS_KEY_ID_}" >> .env && \
    echo "AWS_SECRET_ACCESS_KEY_=${AWS_SECRET_ACCESS_KEY_}" >> .env && \
    echo "REGION_NAME=${REGION_NAME}" >> .env && \
    echo "BUCKET_NAME=${BUCKET_NAME}" >> .env && \
    echo "SGISAPI_KEY=${SGISAPI_KEY}" >> .env && \
    echo "SGISAPI_SECRET=${SGISAPI_SECRET}" >> .env
    echo "MESSAGE_API_KEY=${MESSAGE_API_KEY}" >> .env && \
    echo "MESSAGE_API_SECRET=${MESSAGE_API_SECRET}" >> .env

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
