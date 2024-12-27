FROM python:3.14.0a3-slim
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt 
RUN apt update && apt upgrade -y && apt install ipmitool freeipmi -y
COPY . .

CMD [ "python","-u", "./main.py" ]
