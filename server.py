##UART Server zum Empfangen von Messwerten über die serielle Schnittstelle (Wird auf dem Raspberry Pi empfangen)

import sys
import serial
# import re
# import mysql.connector
# import sqlite3
from datetime import datetime
import glob
import os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  ## Pfad zum Verzeichnis hinzufügen
from main import parse_sensor_data, save_to_mariadb, save_sensor_data, long_zu_zahl, write_to_csv  # Funktionen aus main.py importieren


# Suche nach angeschlossenen ttyUSB Geräten
usb_devices = glob.glob('/dev/ttyUSB*')

if not usb_devices:
    raise Exception("Kein ttyUSB Gerät gefunden")

# Verwende das erste gefundene ttyUSB Gerät
ser = serial.Serial(usb_devices[0], 9600)  # Serielle Schnittstelle öffnen

# Sicherstellen, dass die serielle Verbindung geöffnet ist
if not ser.is_open:
    ser.open()

print("UART Server wurde gestartet.")
print("Warte auf Sensordaten...")


while True:
    if ser.is_open and ser.in_waiting > 0:
        datum = datetime.now() ## Aktuelles Datum und Uhrzeit
        datum_als_long = int(datum.strftime("%Y%m%d%H%M%S")) ## Aktuelles Datum als long-Wert
        line = ser.readline().decode('utf-8').strip()
        data = parse_sensor_data(line)
        for sensor_entry in data:
            save_to_mariadb(current_date=datum, sensor_data=sensor_entry)
            save_sensor_data(datum, sensor_entry)
        for sensor_entry in data:
            print(f"Sensorart = {sensor_entry['sensor_art']}, Sensor Nummer = {sensor_entry['sensor_nummer']}, Vorzeichen = {sensor_entry['sign']}, Wert = {sensor_entry['value']}")

            save_to_mariadb(datum, sensor_entry)
            save_sensor_data(datum, sensor_entry)
            write_to_csv([sensor_entry])

            write_to_csv([sensor_entry])
        print("Datum:", datum)
        print("Datum als long:", datum_als_long)
        print("Datum als Zahl:", long_zu_zahl(datum_als_long))
    elif not ser.is_open:
        print("Serielle Verbindung ist geschlossen. Versuche erneut zu öffnen.")
        ser.open()



