FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE $PORT
WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

COPY . ./

CMD exec uvicorn --workers 1 --host 0.0.0.0 --port $PORT app.main:app

