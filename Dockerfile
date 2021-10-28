FROM python:3.9-slim
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt 
RUN apt update && apt install ipmitool freeipmi -y
COPY . .

CMD [ "python","-u", "./main.py" ]
