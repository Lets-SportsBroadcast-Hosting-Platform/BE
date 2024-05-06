FROM python:3.11.9-slim

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
    BUSSINESS_SERVICE_KEY

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
    echo "BUSSINESS_SERVICE_KEY=${BUSSINESS_SERVICE_KEY}" >> /code/app/.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

WORKDIR /code/app

EXPOSE 80

CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "main:app", "--proxy-headers","--host","0.0.0.0", "--port", "80"]