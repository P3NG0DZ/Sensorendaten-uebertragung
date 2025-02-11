#!/bin/bash
temp_file=$(mktemp)
cp messdaten.csv "$temp_file"

while IFS= read -r line; do
    IFS=',' read -ra fields <<< "$line"
    sensor_data="${fields[1]}${fields[2]}${fields[3]}"
    python main.py "$sensor_data"
done < "$temp_file"

rm "$temp_file"
