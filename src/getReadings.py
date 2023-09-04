import requests
import logging
import configparser
from datetime import datetime
import psycopg2
import time

logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')


def setupUrl():
    url_config = config['url']
    url = url_config['url']
    endpoint = url_config['endpoint']
    lon = url_config['lon']
    lat = url_config['lat']
    units = url_config['units']

    api_config = config['api']
    apikey = api_config['apikey']

    rawUrl = f'{url}{endpoint}lat={lat}&lon={lon}&appid={apikey}&units={units}'

    return rawUrl


def sendRequest():
    response = requests.request('GET', setupUrl(), data='', headers={})

    return response.json()


def convertTimestamp(unix_epoch_time):
    timestamp = datetime.fromtimestamp(unix_epoch_time).isoformat()

    return timestamp


def setDataPayload():

    try:
        logging.info('Getting data from open weather ...')
        data = {
            "main": sendRequest()['weather'][0]['main'],
            "description": sendRequest()['weather'][0]['description'],
            "temperature": sendRequest()['main']['temp'],
            "pressure": sendRequest()['main']['pressure'],
            "humidity": sendRequest()['main']['humidity'],
            "visibility": sendRequest()['visibility'],
            "windspeed": sendRequest()['wind']['speed'],
            "clouds": sendRequest()['clouds']['all'],
            "sunrise": convertTimestamp(sendRequest()['sys']['sunrise']),
            "sunset": convertTimestamp(sendRequest()['sys']['sunset']),
            "city": sendRequest()['name'],
            "lastupdate": datetime.now().isoformat()
        }
        

        logging.info(data)
        return data

    except Exception as err:
        logging.error(err)


def sendReadings():

    db_config = config['db']
    db_host = db_config['host']
    db_port = db_config['port']
    db_name = db_config['database']
    db_username = db_config['username']
    db_password = db_config['password']

    while True:
        try:
            data = setDataPayload()
            logging.info('connection to database ...')
            connection = psycopg2.connect(
                user=db_username, password=db_password, host=db_host, port=db_port,
                database=db_name)

            cursor = connection.cursor()

            sql = """
                    INSERT INTO readings 
                        (main, description, temperature, pressure, humidity, 
                        visibility, windspeed, clouds, sunrise, sunset, city, 
                        lastupdate) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

            values = (
                data['main'],
                data['description'],
                data['temperature'],
                data['pressure'],
                data['humidity'],
                data['visibility'],
                data['windspeed'],
                data['clouds'],
                data['sunrise'],
                data['sunset'],
                data['city'],
                data['lastupdate']
            )

            logging.info('start ingestion ...')
            cursor.execute(sql, values)
            connection.commit()
            cursor.close()
            connection.close()
            logging.info('ingestion done ...')
        except Exception as e:
            logging.error(e)
            logging.error('no database connection ...')

        time.sleep(10)


def main():
    sendReadings()


if __name__ == "__main__":
    main()
