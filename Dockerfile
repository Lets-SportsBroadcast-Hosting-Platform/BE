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
ARG BUSINESS_SERVICE_KEY
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG REGION_NAME
ARG BUCKET_NAME
ARG SGISAPI_KEY
ARG SGISAPI_SECRET

ENV SERVER_SECRET_KEY=${SERVER_SECRET_KEY}
ENV KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID}
ENV KAKAO_RESTAPI_KEY=${KAKAO_RESTAPI_KEY}
ENV NAVER_CLIENT_ID=${NAVER_CLIENT_ID}
ENV NAVER_SECRET_KEY=${NAVER_SECRET_KEY}
ENV DATABASE_HOST=${DATABASE_HOST}
ENV DATABASE_USER=${DATABASE_USER}
ENV DATABASE_PWD=${DATABASE_PWD}
ENV DATABASE_NAME=${DATABASE_NAME}
ENV BUSINESS_SERVICE_KEY=${BUSINESS_SERVICE_KEY}
ENV AWS_ACCESS_KEY_ID_=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY_=${AWS_SECRET_ACCESS_KEY}
ENV REGION_NAME=${REGION_NAME}
ENV BUCKET_NAME=${BUCKET_NAME}
ENV SGISAPI_KEY=${SGISAPI_KEY}
ENV SGISAPI_SECRET=${SGISAPI_SECRET}

WORKDIR /code

# Copy requirements and application code
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

# Create .env file with the environment variables
RUN echo "SERVER_SECRET_KEY=${SERVER_SECRET_KEY}" > /usr/src/app/.env && \
    echo "KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID}" >> /usr/src/app/.env && \
    echo "KAKAO_RESTAPI_KEY=${KAKAO_RESTAPI_KEY}" >> /usr/src/app/.env && \
    echo "NAVER_CLIENT_ID=${NAVER_CLIENT_ID}" >> /usr/src/app/.env && \
    echo "NAVER_SECRET_KEY=${NAVER_SECRET_KEY}" >> /usr/src/app/.env && \
    echo "DATABASE_HOST=${DATABASE_HOST}" >> /usr/src/app/.env && \
    echo "DATABASE_USER=${DATABASE_USER}" >> /usr/src/app/.env && \
    echo "DATABASE_PWD=${DATABASE_PWD}" >> /usr.src/app/.env && \
    echo "DATABASE_NAME=${DATABASE_NAME}" >> /usr/src/app/.env && \
    echo "BUSINESS_SERVICE_KEY=${BUSINESS_SERVICE_KEY}" >> /usr/src/app/.env && \
    echo "AWS_ACCESS_KEY_ID_=${AWS_ACCESS_KEY_ID}" >> /usr/src/app/.env && \
    echo "AWS_SECRET_ACCESS_KEY_=${AWS_SECRET_ACCESS_KEY}" >> /usr/src/app/.env && \
    echo "REGION_NAME=${REGION_NAME}" >> /usr/src/app/.env && \
    echo "BUCKET_NAME=${BUCKET_NAME}" >> /usr/src/app/.env && \
    echo "SGISAPI_KEY=${SGISAPI_KEY}" >> /usr/src/app/.env && \
    echo "SGISAPI_SECRET=${SGISAPI_SECRET}" >> /usr/src/app/.env

# Install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

WORKDIR /usr/src/app
COPY ./app /usr/src/app

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
