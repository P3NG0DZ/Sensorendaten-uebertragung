#!/bin/bash

# Funktion, um zufällige Sensordaten zu generieren
generate_sensor_data() {
    local sensor_types=("T" "H" "P" "L")
    local sensor_type=${sensor_types[$RANDOM % ${#sensor_types[@]}]}
    local sensor_number=$(printf "%02d" $((RANDOM % 100)))
    local sign=$((RANDOM % 2))
    if [ $sign -eq 0 ]; then
        sign="+"
    else
        sign="-"
    fi
    local value=$(printf "%05.1f" $(echo "scale=1; $RANDOM/3276.7" | bc))
    echo ":${sensor_type}${sensor_number}${sign}${value};"
}

# Benutzer nach der Anzahl der zu generierenden Daten fragen
read -p "Wie viele Sensordaten möchten Sie generieren? " count

# Sensordaten generieren und sammeln
sensor_data=""
for ((i = 0; i < count; i++)); do
    sensor_data+=$(generate_sensor_data)
done

# main.py mit den generierten Sensordaten als Übergabeparameter aufrufen
python3 main.py "$sensor_data"