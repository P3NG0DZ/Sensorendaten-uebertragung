#!/bin/bash
all_sensor_data=""
while IFS= read -r line; do
    IFS=',' read -ra fields <<< "$line"
    sensor_data="${fields[1]}${fields[2]}${fields[3]}${fields[4]}"
    all_sensor_data+="$sensor_data "
    python main.py "$sensor_data"
done < messdaten.csv
