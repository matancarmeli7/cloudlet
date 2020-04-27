FROM python:3.8-alpine 

RUN pip install requests schedule

ADD . ./app
WORKDIR /app

CMD ["python", "-u", "DownloadClient.py"]
