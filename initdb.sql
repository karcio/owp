CREATE DATABASE readings;
CREATE USER dbuser;
ALTER USER dbuser WITH ENCRYPTED PASSWORD 'pa88w0rd';
GRANT ALL PRIVILEGES ON DATABASE readings TO dbuser;
\c readings;
CREATE TABLE readings(id serial PRIMARY KEY, temperature NUMERIC NULL, pressure NUMERIC NULL, humidity VARCHAR (30) NOT NULL, lastupdate TIMESTAMP NOT NULL);
