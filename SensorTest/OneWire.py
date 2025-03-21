## Testen des OneWire Sensors mit DS18B20
import os
import glob
import time
import sys
# ...weitere benötigte Module...

## Initialisierung des OneWire Busses
temperatur = 0
os.system('modprobe w1-gpio')   # Lade das w1-gpio Modul
os.system('modprobe w1-therm')   # Lade das w1-therm Modul

## Festlegen des Basisverzeichnisses für den Sensor
base_dir = '/sys/bus/w1/devices/'
# Filtern der Ordner, die die Datei 'w1_slave' enthalten, um den Sensor zu finden
device_folders = [folder for folder in glob.glob(base_dir + '*') if os.path.exists(os.path.join(folder, 'w1_slave'))]
if device_folders:
    device_folder = device_folders[0]
    device_file = os.path.join(device_folder, 'w1_slave')
else:
    print("Kein Sensor gefunden!")
    sys.exit(1)

## Funktion zum Auslesen der Rohdaten vom Sensor
def read_temp_raw():
    # Öffnet die Sensor-Datei und liest alle Zeilen ein
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

## Funktion zum Auslesen und Verarbeiten der Temperaturdaten
def read_temp():
    lines = read_temp_raw()  # Lese die rohen Sensordaten
    # Warte, bis die erste Zeile 'YES' bestätigt, dass die Daten korrekt gelesen wurden
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0  # Konvertiert den Wert in Grad Celsius
        return temp_c

## Endlosschleife: Liest kontinuierlich die Temperatur aus und gibt sie aus
while True:
    temperatur = read_temp()
    print("Temperatur: ", temperatur, "°C")
    time.sleep(1)
