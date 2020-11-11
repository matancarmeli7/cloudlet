FROM centos/python-36-centos7
USER root
RUN userdel saslauth 
RUN useradd -u 999 -ms /bin/bash minio-test
RUN mkdir -p /minio-test/src/config
WORKDIR /minio-test/src
COPY app.py .
RUN pip3 install requests minio urllib3 kubernetes ipaddress&& pip3 install --upgrade requests
RUN chmod 777 /minio-test -R && chown minio-test:minio-test /minio-test -R
USER minio-test
CMD python app.py
