##UART Client um Messwerte an den Server zu senden (Wird auf dem Raspberry Pi ausgeführt.)

import glob
import serial
import re
import time

data_limit = 10  # Limit für die Anzahl der Sensordaten
current_data = 0  # Zähler für die Anzahl der Sensordaten


# Suche nach angeschlossenen ttyUSB Geräten
usb_devices = glob.glob('/dev/ttyUSB*')

if not usb_devices:
    raise Exception("Kein ttyUSB Gerät gefunden")

# Verwende das erste gefundene ttyUSB Gerät
ser = serial.Serial(usb_devices[0], 9600)  # Serielle Schnittstelle öffnen

while current_data < data_limit:
    print("Bitte geben die Sensordaten ein:")
    sensor_data = input().strip()  # Eingabe der Sensordaten

    # Sicher gehen dass das Muster richtig ist
    # pattern = r"(T)(\d{2})([+-])(\d+\.\d+)"
    # if not re.match(pattern, sensor_data):
    #     #print("Ungültiges Sensordatenformat. Bitte erneut eingeben.")
    #     continue

    ser.write((sensor_data + '\n').encode())  # Newline am Ende hinzufügen
    print("Sensordaten gesendet:", sensor_data)
    current_data += 1  # Zähler erhöhen
    time.sleep(1)  # Wartezeit von 1 Sekunde

print("Datenlimit erreicht. Programm beendet.")
   

