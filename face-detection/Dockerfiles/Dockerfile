#FROM docker.io/tiangolo/python-machine-learning:cuda9.1-python3.7
#FROM nvidia/opencl:runtime-ubuntu18.04
FROM nvidia/opencl:runtime-centos7

RUN adduser --disabled-password --gecos '' app_gpu

WORKDIR /home/app_gpu

RUN chmod 777 /home/app_gpu

ADD . /home/app_gpu

#RUN apt update
#RUN apt install python3 python3-pip libsm6 libxrender1 libxtst6 -y 
RUN yum install libSM libXrender libXevie python3 -y

RUN pip3 install -r req.txt

RUN chown app_gpu:app_gpu ./ -R

USER app_gpu

CMD ["python3" , "main.py"]
