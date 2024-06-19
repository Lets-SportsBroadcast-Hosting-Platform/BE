FROM --platform=linux/amd64 python:3.11.9-slim as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Requirements and application code
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

# Install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

WORKDIR /usr/src/app
COPY ./app /usr/src/app
COPY .env /usr/src/app/.env  
# Ensure .env is copied to the correct path

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
