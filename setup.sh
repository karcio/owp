#!/bin/bash

python3 -m venv virtenv
source virtenv/bin/activate
pip install -r requirements.txt
python getReadings.py
