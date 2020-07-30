FROM python:3.6-alpine3.11
RUN adduser --disabled-password --gecos '' minio-test
RUN mkdir -p /minio-test/src/config
RUN chmod 777 /minio-test -R
RUN chown minio-test:minio-test /minio-test -R
COPY app.py /minio-test/src
WORKDIR /minio-test/src
RUN pip3 install requests schedule minio flask
EXPOSE 5000
USER minio-test
CMD ["python", "app.py"]
