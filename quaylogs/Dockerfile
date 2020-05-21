FROM python:3.5.9-alpine3.11
RUN adduser --disabled-password --gecos '' app_python
WORKDIR /home/app_python
RUN mkdir /home/app_python/conf
RUN chmod 777 /home/app_python && chmod 777 conf
ADD quaylogs.py /home/app_python/ && script_runs /home/app_python/ && prameters /home/app_python/
RUN pip install schedule requests
RUN chown app_python:app_python ./ -R
USER app_python
CMD ["/bin/sh" , "script_runs"]
