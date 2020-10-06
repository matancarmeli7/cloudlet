FROM python:3.6-slim-stretch
RUN adduser --disabled-password --gecos '' quay-test
RUN mkdir -p /quaytest/config
ADD . /quaytest
WORKDIR /quaytest
RUN mv oc /usr/bin
RUN ls
RUN chown -R quay-test:quay-test /quaytest
RUN chmod 777 /quaytest
RUN pip3 install requests kubernetes
USER quay-test
#CMD ["/bin/sh", "./start.sh"]
#CMD ["python", "app.py"]
CMD sh ./start.sh && python app.py
