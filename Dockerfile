FROM python:3

EXPOSE 5432

#COPY requirements.txt /app
#COPY initdb.sql /app
#COPY getReadings.py /app
#COPY setup.sh /app

ADD requirements.txt requirements.txt
ADD setup.sh setup.sh
ADD getReadings.py getReadings.py
ADD initdb.sql dbinit.sql

RUN apt-get update -y && apt-get upgrade -y

CMD ./setup.sh
