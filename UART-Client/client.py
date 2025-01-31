##UART Client um Messwerte an den Server zu senden (Wird auf dem Raspberry Pi ausgeführt.)

import glob
import serial
import re
import time


# Suche nach angeschlossenen ttyUSB Geräten
usb_devices = glob.glob('/dev/ttyUSB*')

if not usb_devices:
    raise Exception("Kein ttyUSB Gerät gefunden")

# Verwende das erste gefundene ttyUSB Gerät
ser = serial.Serial(usb_devices[0], 9600)  # Serielle Schnittstelle öffnen

while True:
   print("Bitte geben die Sensordaten ein:")
   sensor_data = input()

   # Sicher gehen dass das Muster richtig ist
   pattern = r"(T)(\d{2})([+-])(\d+\.\d+)"
   if not re.match(pattern, sensor_data):
       print("Ungültiges Sensordatenformat. Bitte erneut eingeben.")
       continue

ser.write(sensor_data.encode())  # Sensordaten an den Server senden
print("Sensordaten gesendet:", sensor_data)
time.sleep(1)  # Wartezeit von 1 Sekunde
   

