FROM centos/python-36-centos7
USER root
RUN userdel saslauth
RUN useradd -u 999 -ms /bin/bash quaylogs
RUN mkdir -p /quaylogs/src/config
WORKDIR /quaylogs/src
COPY oc app.py ./
RUN pip3 install requests kubernetes
RUN chmod 777 /quaylogs -R && chown quaylogs:quaylogs /quaylogs -R
USER quaylogs
CMD python app.py
