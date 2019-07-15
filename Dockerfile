FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

RUN apk add make gcc musl-dev libffi-dev openssl-dev && \
pip install flask paramiko && \
echo "192.168.78.58 poweredge" >> /etc/hosts
COPY ./ /app
