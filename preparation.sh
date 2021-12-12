#!/bin/bash 

sudo apt-get install python3-venv tor
python3 -m venv .venv

source .venv/bin/activate

sudo apt-get install python3-pip
pip install -r requirements.txt