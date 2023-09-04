# owp (openweather project)

## manual start application

1. install python3

2. create virt env

```
python3 -m venv virtenv
```

3. source virt env

```
source virtenv/bin/activate
```

4. install dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

5. move `config.properties` to `config.ini` and update following:

```
[database]
host =
port =
database =
username =
password =

[url]
url = https://api.openweathermap.org
endpoint = /data/2.5/weather?
lon =
lat =
units = metric

[api]
apikey =
```

6. Create (postgres) database for readings

```
CREATE DATABASE owpdb;
CREATE USER dbuser;
ALTER USER dbuser WITH ENCRYPTED PASSWORD 'password';
ALTER DATABASE owpdb OWNER TO dbuser;
\c owpdb;
CREATE TABLE readings(id serial PRIMARY KEY, main VARCHAR(10), description VARCHAR(15), temperature NUMERIC NULL, pressure NUMERIC NULL, humidity NUMERIC NULL, visibility NUMERIC NULL, windspeed NUMERIC NULL, clouds NUMERIC NULL, sunrise TIMESTAMP NULL, sunset TIMESTAMP NULL, city VARCHAR (10), rain SMALLINT NULL, snow SMALLINT NULL, clear SMALLINT NULL, thunderstorm SMALLINT NULL,lastupdate TIMESTAMP NOT NULL);
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dbuser;
GRANT ALL PRIVILEGES ON DATABASE owpdb TO dbuser;
```

7. run script

```
python src/getReadings.py
```

## docker-compose run application

**in progress**

```
docker-compose build
docker-compose up -d
```
