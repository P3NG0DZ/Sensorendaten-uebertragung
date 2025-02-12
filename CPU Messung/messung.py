#Python Programm für die CPU Temperaturmessung auf einem Raspberry Pi. Wird am ende über UART gesendet.

import os
import sys
import time
import serial
import glob


i = 10 # Anzahl der Messungen die durchgeführt werden sollen

sensor_name = "P01" ## Sensorname
wert = 0 ## Wert



# Suche nach angeschlossenen ttyUSB Geräten
usb_devices = glob.glob('/dev/ttyUSB*')

if not usb_devices:
    raise Exception("Kein ttyUSB Gerät gefunden")

# Verwende das erste gefundene ttyUSB Gerät
ser = serial.Serial(usb_devices[0], 9600)  # Serielle Schnittstelle öffnen

# Sicherstellen, dass die serielle Verbindung geöffnet ist
if not ser.is_open:
    ser.open()


def get_cpu_temperature(): ## Funktion um die CPU-Temperatur zu messen
    res = os.popen("vcgencmd measure_temp").readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))



print("CPU Temperaturmessung")
print("Der Wert wird so ausgegeben: Datum, Sensorname, Wert")
print("Beispiel: 2021-07-23 12:00:00, P01, 50.0")
print("Der Server wird dann die Daten empfangen und die Funktionen aus main.py aufrufen.")
print("Wert und das alles wird Beispiel so als UART gesendet: T01+50.0")

print("Messvorgang wird gestartet...")

##Messvorgang starten und die Daten über UART senden
for _ in range(i):
    wert = get_cpu_temperature()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    data = f"{timestamp}, {sensor_name}, {wert}"
    print(data)
    uart_data = f"{sensor_name}+{wert}\n"
    ser.write(uart_data.encode('utf-8'))
    time.sleep(1)  # Wartezeit zwischen den Messungen
  
print("Messvorgang wurde erfolgreich beendet.")
ser.close()  # Serielle Schnittstelle schließen






