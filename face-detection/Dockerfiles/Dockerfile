FROM docker.io/tiangolo/python-machine-learning

RUN adduser --disabled-password --gecos '' app_gpu

WORKDIR /home/app_gpu

RUN chmod 777 /home/app_gpu

ADD . /home/app_gpu

RUN ls -l 

RUN pip install -r req.txt

RUN chown app_gpu:app_gpu ./ -R

RUN ls -l

USER app_gpu

RUN ls -l

CMD ["python3" , "main.py"]

