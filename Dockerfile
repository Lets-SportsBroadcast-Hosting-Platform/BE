FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 환경 변수 파일 복사
COPY app/.env /code/app/.env

WORKDIR /code

# .env 파일 로드
ENV $(cat /app/.env | xargs)

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

EXPOSE 80

CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "main:app", "--proxy-headers","--host","0.0.0.0", "--port", "80"]