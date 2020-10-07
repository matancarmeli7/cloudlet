FROM centos/python-36-centos7
USER root
RUN userdel saslauth 
RUN useradd -u 999 -ms /bin/bash minio-test
RUN mkdir -p /minio-test/src/config
RUN chmod 777 /minio-test -R
COPY app.py /minio-test/src
WORKDIR /minio-test/src
RUN pip3 install requests schedule minio urllib3
RUN chown minio-test:minio-test /minio-test -R
USER minio-test
CMD ["python", "app.py"]
