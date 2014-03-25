#!/bin/sh

apt-get update
apt-get install git mongodb python3 python-pip build-essential python-dev
git clone https://github.com/luisivan/anondoge.git
cd anondoge/server
pip install -r requirements.txt