#!/bin/bash

apt update
apt -y install git
apt -y install python3.7
apt -y install python3-pip
apt -y install libpq-dev
cd /usr/local/bin/auth
#pip3 install libpq-dev
#pip3 install psycopg2-binary
#pip3 install psycopg2
#pip3 install Flask
#pip3 install pyjwt
#pip3 install python-dotenv
pip3 install -r requirements.txt
python3 testflask.py
