FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
COPY ./requirements.txt .
COPY ./app /app
COPY ./app/nginx_default.conf /etc/nginx/conf.d
RUN pip install -r ./requirements.txt
