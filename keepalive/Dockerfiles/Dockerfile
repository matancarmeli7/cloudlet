FROM python:3.5.9-alpine3.11

RUN adduser --disabled-password --gecos '' app_python

WORKDIR /home/app_python

RUN chmod 777 /home/app_python

RUN mkdir /home/app_python/conf

RUN chmod 777 conf

ADD keepalive.py /home/app_python/

ADD script_runs /home/app_python/

ADD prameters_script /home/app_python/

RUN pip install schedule

RUN pip install requests

RUN chown app_python:app_python ./ -R

RUN ls -l

USER app_python

RUN ls -l

CMD ["/bin/sh" , "script_runs"]

