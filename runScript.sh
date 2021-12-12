#!/bin/bash 
source .venv/bin/activate

while true
do
sleep 1
python3 autoreg.py
echo "Перезагружаем tor..."
sudo systemctl restart tor
done