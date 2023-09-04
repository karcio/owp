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

timeout = 300


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

        symbol = sendRequest()['weather'][0]['main']
        
        weather_mappings = {
            "rain": ["rain","drizzle"],
            "thunderstorm": ["thunderstorm"],
            "snow": ["snow"],
            "clear": ["clear"]
        }

        symbol_lower = symbol.lower()

        rain = 1 if any(
            cond in symbol_lower for cond in weather_mappings["rain"]) else 0
        snow = 1 if any(
            cond in symbol_lower for cond in weather_mappings["snow"]) else 0
        clear = 1 if any(
            cond in symbol_lower for cond in weather_mappings["clear"]) else 0
        thunderstorm = 1 if any(
            cond in symbol_lower for cond in weather_mappings["thunderstorm"]) else 0


        data = {
            "main": symbol, 
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
            "rain": rain,
            "thunderstorm": thunderstorm,
            "snow": snow,
            "clear": clear,
            "lastupdate": datetime.now().isoformat()
        }
        

        logging.info(data)
        return data

    except Exception as err:
        logging.error(err)


def sendReadings():
    db_config = config['database']
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
                        rain, thunderstorm, snow, clear, lastupdate) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                data['rain'],
                data['thunderstorm'],
                data['snow'],
                data['clear'],
                data['lastupdate']
            )

            logging.info('start ingestion ...')
            cursor.execute(sql, values)
            connection.commit()
            cursor.close()
            connection.close()
            logging.info('ingestion done ...')
            logging.info(f'waiting {timeout} seconds for next query ...')
        except Exception as e:
            logging.error(e)
            logging.error('no database connection ...')

        time.sleep(timeout)


def main():
    sendReadings()


if __name__ == "__main__":
    main()
