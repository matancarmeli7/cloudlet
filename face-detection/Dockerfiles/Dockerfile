FROM nvidia/opencl:runtime-centos7

RUN useradd -ms /bin/bash app_gpu

WORKDIR /home/app_gpu

RUN chmod 777 /home/app_gpu

ADD . /home/app_gpu
 
RUN yum install libSM libXrender libXevie python3 -y

RUN pip3 install -r req.txt

RUN chown app_gpu:app_gpu ./ -R

USER app_gpu

EXPOSE 5000

CMD ["python3" , "main.py"]
