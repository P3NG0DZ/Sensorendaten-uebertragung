## Testen des OneWire Sensors mit DS18B20
import os
import glob
import time
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from main import parse_sensor_data, save_sensor_data, save_to_mariadb, write_to_csv, long_zu_zahl
from datetime import datetime


# Sensorname für die Datenbank
sensorname = "T01"


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

     
    def format_pattern(sensor, value): # Funktion zur Formatierung des Sensorsignals in ein bestimmtes Muster
        return f":{sensor}{value:+07.1f};"
    
    pattern_temp = format_pattern(sensorname, temperatur) # Formatierung der Temperaturdaten
    print("Pattern:", pattern_temp)
    sensor_data_list = parse_sensor_data(pattern_temp) # Zerlege das Muster in einen Sensordatensatz
    if sensor_data_list:
        sensor_entry = sensor_data_list[0]
        current_time = datetime.now()  # Ermittele die aktuelle Zeit
        try:
            save_to_mariadb(current_time, sensor_entry) # Speichere die Sensordaten in einer MariaDB-Datenbank
        except Exception as err:
            print("Fehler beim Speichern in MariaDB:", err)
        write_to_csv([sensor_entry]) # Speichere die Sensordaten in einer CSV-Datei

    

    time.sleep(1)
