FROM python:3.12.5-alpine

WORKDIR /usr/src/app
COPY requirements.txt .
COPY . .
RUN apt-get update && apt-get install nodejs npm python3-dev build-essential default-libmysqlclient-dev -y

RUN pip install waitress
RUN pip install -r requirements.txt

EXPOSE 3003
CMD exec waitress-serve --port=3003 wsgi:app