FROM python:3.6-alpine3.11
RUN mkdir -p /quay-logs/src/config
ADD . /quay-logs/src
USER root
WORKDIR /quay-logs/src
RUN pip3 install requests schedule
COPY app.py /quay-logs/src
CMD ["python", "app.py"]
