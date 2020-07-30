FROM python:3.6-alpine3.11
RUN mkdir -p /argocd_to_splunk/src/config
ADD . /argocd_to_splunk/src
USER root
WORKDIR /argocd_to_splunk/src
RUN pip3 install requests schedule
COPY app.py /argocd_to_splunk/src
CMD ["python", "app.py"]
