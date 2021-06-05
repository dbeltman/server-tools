FROM python:3.8.3-slim
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt && apt update && apt install ipmitool -y
COPY . .

CMD [ "python", "./main.py" ]
