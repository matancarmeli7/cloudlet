FROM python:3.8.5-alpine

WORKDIR /teston

COPY ./teston.py .

RUN addgroup -S dod && adduser -S dod -G dod

USER dod

CMD ["python", "-u", "teston.py"]

