FROM python:3.8.5-alpine

WORKDIR /app_argo

RUN pip install httpx requests

COPY ./app_argo.py .

COPY ./config.py .

RUN addgroup -S dod && adduser -S dod -G dod

USER dod

CMD ["python", "-u", "app_argo.py"]
