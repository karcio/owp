CREATE DATABASE owpdb;
CREATE USER dbuser;
ALTER USER dbuser WITH ENCRYPTED PASSWORD 'pa88w0rd';
ALTER DATABASE owpdb OWNER TO dbuser;
\c owpdb;
CREATE TABLE readings(id serial PRIMARY KEY, temperature NUMERIC NULL, pressure NUMERIC NULL, humidity NUMERIC NULL, windspeed NUMERIC NULL, weather VARCHAR (10), weatherdetailed VARCHAR (20), city VARCHAR (15), lastupdate TIMESTAMP NOT NULL);
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dbuser;
GRANT ALL PRIVILEGES ON DATABASE owpdb TO dbuser;
