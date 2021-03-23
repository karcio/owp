from pyowm import OWM
import logging
import psycopg2
from datetime import datetime
import time

logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)

while True:
    owm = OWM('8d0d43256b8bfb855fd1750d1bd612cd')

    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place('Celbridge,IE')
        w = observation.weather
        humidity = w.humidity
        temperature = w.temperature('celsius')['temp']
        pressure = w.pressure['press']

        data = {"temp": temperature, "press": pressure, "humi": humidity}
        logging.info(data)

    except:
        logging.error(' no connection to owm ...')

    try:

        connection = psycopg2.connect(
            user="dbuser", password="pa88w0rd", host="localhost", port="5432", database="readings")
        cursor = connection.cursor()

        sql = "insert into readings (temperature, pressure, humidity, lastupdate) values ('" + str(data['temp']) + "', '" + str(
            data['press']) + "', '" + str(data['humi']) + "', '" + datetime.now().isoformat() + "')"

        logging.info('start ingestion ...')
        cursor.execute(sql)
        logging.info(sql)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(' ingestion done ...')
    except:
        logging.error(' no connection ...')

    time.sleep(300)
