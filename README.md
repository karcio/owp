# owp

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

5. edit env `config.properties`
```
[APP]
API_KEY=
CITY=

[DB]
HOST=
PORT=
DATABASE=
DBUSER=
DBPASSWORD=
```

6. run script
```
python getReadings.py
```

## docker-compose run application
```
docker-compose build
docker-compose up -d
```