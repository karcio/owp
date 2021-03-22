FROM python:3

EXPOSE 8080
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update -y && apt upgrade -y
RUN apt install vim -y
COPY . .

CMD [ "python", "./getReadings.py" ]
