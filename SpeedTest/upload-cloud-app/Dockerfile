FROM python:3.8-alpine

RUN pip install requests

ADD . /app
WORKDIR /app

CMD ["python", "-u", "Server.py"]
