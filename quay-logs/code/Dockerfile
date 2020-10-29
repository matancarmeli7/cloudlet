FROM centos/python-36-centos7
USER root
RUN userdel saslauth
RUN useradd -u 999 -ms /bin/bash quaylogs
RUN mkdir -p /quaylogs/src/config
WORKDIR /quaylogs/src
COPY oc app.py start.sh .
RUN mv oc /usr/bin
RUN pip3 install requests kubernetes
RUN chmod 777 /quaylogs -R && chown quaylogs:quaylogs /quaylogs -R
USER quaylogs
CMD sh ./start.sh && python app.py
