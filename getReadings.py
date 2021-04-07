from pyowm import OWM
import logging
import psycopg2
from datetime import datetime
import time
#from config import configuration

logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)

API_KEY = '8d0d43256b8bfb855fd1750d1bd612cd'
CITY = 'Celbridge,IE'
HOST = '192.168.178.71'
PORT = '5433'
DATABASE = 'owpdb'
DBUSER = 'dbuser'
DBPASSWORD = 'pa88w0rd'


while True:
    owm = OWM(API_KEY)

    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(CITY)
        w = observation.weather
        humidity = w.humidity
        temperature = w.temperature('celsius')['temp']
        pressure = w.pressure['press']

        data = {"temp": temperature, "press": pressure, "humi": humidity}
        logging.info(data)

    except:
        logging.error(' no connection to owm ...')
    
    try:

        connection = psycopg2.connect(user=DBUSER, password=DBPASSWORD, host=HOST, port=PORT, database=DATABASE)
        cursor = connection.cursor()

        sql = "insert into readings (temperature, pressure, humidity, lastupdate) values ('" + str(data['temp']) + "', '" + str(data['press']) + "', '" + str(data['humi']) + "', '" + datetime.now().isoformat() + "')"

        logging.info('start ingestion ...')
        cursor.execute(sql)
        logging.info(sql)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info(' ingestion done ...')
    except:
        logging.error(' no database connection ...')

    time.sleep(300)
