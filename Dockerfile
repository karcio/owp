FROM python:3

ADD requirements.txt requirements.txt
ADD setup.sh setup.sh
ADD getReadings.py getReadings.py
ADD initdb.sql dbinit.sql

RUN apt-get update -y && apt-get upgrade -y

CMD ./setup.sh
