#!/bin/bash

apt update
apt -y install git
apt -y install python3.7
apt -y install python3-pip
cd /usr/local/bin/httpserv/
pip3 install -r requirements.txt
python3 httpf.py
