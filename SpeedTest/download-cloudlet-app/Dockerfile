FROM python:2.7.17-alpine3.11

RUN pip install requests schedule

ADD ./download-cloudlet-app /app
WORKDIR /app

CMD python speedtest.py
