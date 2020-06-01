FROM python:3.8-alpine

RUN pip install schedule

ADD . /app
WORKDIR /app

CMD ["python", "-u", "Client.py" ]
