FROM python:3.5-alpine
#FROM resin/raspberry-pi-alpine-python:latest

COPY . /opt/app
WORKDIR /opt/app

RUN apk update
RUN apk add build-base libxml2-dev libxslt-dev
RUN pip install -r requirements.txt

CMD ["python3","bot.py"]
