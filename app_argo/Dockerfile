FROM python:3.8.5-alpine

RUN addgroup -S dod && adduser -S dod -G dod

WORKDIR -p /app_argo/config

RUN pip install httpx requests

COPY ./app_argo.py .

USER dod

CMD ["python", "-u", "app_argo.py"]
