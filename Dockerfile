FROM python:3.9
COPY requirements.txt .
COPY . .
WORKDIR /usr/src/app

RUN apt-get update && apt-get install nodejs npm python3-dev build-essential default-libmysqlclient-dev -y

RUN pip install waitress
RUN pip install -r requirements.txt

EXPOSE 3003
CMD exec waitress-serve --port=3003 wsgi:app