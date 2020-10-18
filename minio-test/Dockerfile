FROM centos/python-36-centos7
USER root
RUN userdel saslauth 
RUN useradd -u 999 -ms /bin/bash minio-test
RUN mkdir -p /minio-test/src/config
WORKDIR /minio-test/src
COPY oc app.py start.sh .
RUN mv oc /usr/bin && touch meshi
RUN pip3 install requests schedule minio urllib3 kubernetes
RUN chmod 777 /minio-test -R && chown minio-test:minio-test /minio-test -R
USER minio-test
CMD sh ./start.sh && python app.py
