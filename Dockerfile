FROM python:3

WORKDIR /app

ADD requirements.txt requirements.txt
ADD setup.sh setup.sh
ADD getReadings.py getReadings.py
ADD initdb.sql initdb.sql
ADD config.py config.py
ADD config.properties config.properties

RUN apt-get update -y && apt-get upgrade -y

CMD ./setup.sh
