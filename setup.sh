#!/bin/bash

python3 -m venv virtenv
source virtenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python src/getReadings.py
