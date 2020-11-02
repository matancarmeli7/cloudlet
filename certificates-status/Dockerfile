FROM centos/python-36-centos7
USER root
RUN userdel saslauth 
RUN useradd -u 999 -ms /bin/bash crt-status
RUN mkdir -p /certificates-status/src/config
WORKDIR /certificates-status/src
COPY app.py .
RUN pip3 install psycopg2 urllib3 requests
RUN chmod 777 /certificates-status -R && chown crt-status:crt-status /certificates-status -R
USER crt-status
CMD python app.py
