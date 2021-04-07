FROM python:3

#EXPOSE 5433

#COPY requirements.txt /app
#COPY initdb.sql /app
#COPY getReadings.py /app
#COPY setup.sh /app

#RUN useradd dbuser
#RUN mkdir -p /var/lib/postgresql/data
#RUN chown -R dbuser:dbuser /var/lib/postgresql/data

ADD requirements.txt requirements.txt
ADD setup.sh setup.sh
ADD getReadings.py getReadings.py
ADD initdb.sql dbinit.sql

RUN apt-get update -y && apt-get upgrade -y

CMD ./setup.sh
