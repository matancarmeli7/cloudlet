FROM python:3.6-alpine3.11
RUN adduser --disabled-password --gecos '' app-test
RUN mkdir -p /app-test-to-splunk/src/config
RUN chmod 777 /app-test-to-splunk -R
RUN chown app-test:app-test /app-test-to-splunk -R
COPY app.py /app-test-to-splunk/src
WORKDIR /app-test-to-splunk/src
RUN pip3 install requests schedule
USER app-test
CMD ["python", "app.py"]
