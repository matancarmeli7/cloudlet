FROM python:2.7.17-alpine3.11

RUN pip install requests schedule

ADD ./app /app
WORKDIR /app

CMD python Salty.py
