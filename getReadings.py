from pyowm import OWM
import logging
import psycopg2
from datetime import datetime
import time
from config import configuration

logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)

API_KEY = configuration().getApiKey()
CITY = configuration().getCity()
HOST = configuration().getHost()
PORT = configuration().getPort()
DATABASE = configuration().getDatabase()
DBUSER = configuration().getDatabaseUser()
DBPASSWORD = configuration().getDatabasePass()

while True:
    owm = OWM(API_KEY)

    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(CITY)
        w = observation.weather
        weather = w.status
        humidity = w.humidity
        temperature = w.temperature('celsius')['temp']
        pressure = w.pressure['press']
        wind = w.wind()['speed']

        data = {"temp": temperature, "press": pressure,
                "humi": humidity, "wind_speed": wind, "weather": weather}
        logging.info(data)
        logging.info(' data received ...')

    except:
        logging.error(' no connection to owm ...')

    try:

        connection = psycopg2.connect(
            user=DBUSER, password=DBPASSWORD, host=HOST, port=PORT, database=DATABASE)
        cursor = connection.cursor()

        sql = "insert into readings (temperature, pressure, humidity, windspeed, weather, lastupdate) values ('" + str(
            data['temp']) + "', '" + str(data['press']) + "', '" + str(data['humi']) + "', '" + str(data['wind_speed']) + "', '" + str(data['weather']) + "', '" + datetime.now().isoformat() + "')"

        logging.info(' start ingestion ...')
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(' ingestion done ...')
    except:
        logging.error(' no database connection ...')

    time.sleep(300)
