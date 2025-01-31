##UART Server zum Empfangen von Messwerten über die serielle Schnittstelle (Wird auf dem Raspberry Pi empfangen)

import serial
import re
import mysql.connector
import sqlite3
from datetime import datetime
from main import parse_data, save_to_mariadb, save_sensor_data, long_zu_zahl
import glob


# Suche nach angeschlossenen ttyUSB Geräten
usb_devices = glob.glob('/dev/ttyUSB*')

if not usb_devices:
    raise Exception("Kein ttyUSB Gerät gefunden")

# Verwende das erste gefundene ttyUSB Gerät
ser = serial.Serial(usb_devices[0], 9600) ## Serielle Schnittstelle öffnen


datum = datetime.now() ## Aktuelles Datum und Uhrzeit
datum_als_long = int(datum.strftime("%Y%m%d%H%M%S")) ## Aktuelles Datum als long-Wert


while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        data = parse_data(line)
        save_to_mariadb(data)
        save_sensor_data(data)
        print(data)
        print("Datum:", datum)
        print("Datum als long:", datum_als_long)
        print("Datum als Zahl:", long_zu_zahl(datum_als_long))
       


