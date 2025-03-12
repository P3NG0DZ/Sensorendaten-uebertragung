import Adafruit_ADS1x15
import time
import os
import sys
from main import parse_sensor_data, save_sensor_data, save_to_mariadb, write_to_csv, long_zu_zahl
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


#A0 -> Potentiometer
#A1 -> LDR
#A2 -> PTC


##Sensornamen fuer die Datenbank
poti = "PT1"
ldr = "LD1"
ntc = "NT1"



adc = Adafruit_ADS1x15.ADS1115(busnum=1) # Wird auf Bus 1 initialisiert
GAIN = 1 # Verstärkung des ADCs
DATA_RATE = 860  # Maximale Datenrate für schnellere Konversionen

# Umrechnungsfaktor: 0.125 mV pro Digit (bei GAIN=1 und ±4.096V Range)
CONV_FACTOR = 0.125

# Initialisiere Messzähler
messung = 0

while True:
    value1 = adc.read_adc(0, gain=GAIN, data_rate=DATA_RATE) #Wert des LDRs wird ausgelesen
    value2 = adc.read_adc(1, gain=GAIN, data_rate=DATA_RATE) #Wert des Potentiometers wird ausgelesen
    value3 = adc.read_adc(2, gain=GAIN, data_rate=DATA_RATE) #Wert des PTCs wird ausgelesen

    # Berechnung der Spannungswerte in mV
    poti_mV = value1 * CONV_FACTOR
    ldr_mV  = value2 * CONV_FACTOR
    ntc_mV  = value3 * CONV_FACTOR

    # Dummy-Umrechnung in Ohm (hier übernehmen wir den mV-Wert als symbolischen Widerstandswert)
    poti_ohm = poti_mV
    ldr_ohm  = ldr_mV
    ntc_ohm  = ntc_mV

    # Weitere Umrechnung:
    # Poti: 1 kOhm entspricht 10 cm => 1 Ohm entspricht 0.1 mm
    poti_mm = round(poti_ohm * 0.1, 2)
    # NTC: Umrechnung in °C (hier:  °C = ntc_mV * 0.1)
    ntc_deg = round(ntc_mV * 0.1, 2)
    # LDR: Umrechnung in Lux (hier verwenden wir einen Faktor von 1.0, d.h. Lux = ldr_mV)
    ldr_lux = round(ldr_mV * 1.0, 2)

    # Ausgabe in drei Zeilen:
    # Zeile 1: Digitale Werte und Spannungswerte in mV
    # Reihenfolge: Poti, LDR, NTC
    # Zeile 2: Umrechnung in Ohm
    # Zeile 3: Umrechnung in physikalische Größen (Poti in mm, LDR in Lux, NTC in °C)
    print("Messung: {0}  Poti = {1} digit = {2:.1f} mV  LDR = {3} digit = {4:.1f} mV  NTC = {5} digit = {6:.1f} mV"
          .format(messung, value1, poti_mV, value2, ldr_mV, value3, ntc_mV))
    print("=>  Poti = {0:.1f} Ohm,  LDR = {1:.1f} Ohm,  NTC = {2:.1f} Ohm".format(poti_ohm, ldr_ohm, ntc_ohm))
    print("=>  Poti = {0:.1f} mm,  LDR = {1:.1f} Lux,  NTC = {2:.1f} °C".format(poti_mm, ldr_lux, ntc_deg))
    print("---------------------------------------------------------")

    # Funktion zur Formatierung des Sensorsignals in ein bestimmtes Muster
    def format_pattern(sensor, value):
        return f":{sensor}{value:+07.1f};"

    # Formatierung der Messwerte für Poti, LDR und NTC
    pattern_poti = format_pattern(poti, poti_mm)
    pattern_ldr  = format_pattern(ldr, ldr_lux)
    pattern_ntc  = format_pattern(ntc, ntc_deg)

    # Speichere die einzelnen Sensordaten separat
    for sensor_pattern in [pattern_poti, pattern_ldr, pattern_ntc]:
        print("Pattern:", sensor_pattern)
        # Zerlege das Muster in einen Sensordatensatz (es wird angenommen, dass die Funktion
        # parse_sensor_data eine Liste mit einem Eintrag zurückgibt, wenn nur ein Sensorwert übergeben wird)
        sensor_data_list = parse_sensor_data(sensor_pattern)
        if sensor_data_list:
            sensor_entry = sensor_data_list[0]
            current_time = datetime.now()  # Ermittele die aktuelle Zeit
            # Speichere den Sensordatensatz lokal (sofern gewünscht)
            # save_sensor_data(current_time, sensor_entry)
            try:
                # Versuche, die Sensordaten in einer MariaDB-Datenbank zu speichern
                save_to_mariadb(current_time, sensor_entry)
            except Exception as err:
                # Gib eine Fehlermeldung aus, falls das Speichern in der Datenbank fehlschlägt
                print("Fehler beim Speichern in MariaDB:", err)
    
            # Speichere die Sensordaten in einer CSV-Datei
            #write_to_csv([sensor_entry])

    messung += 1  # Messzähler erhöhen
    time.sleep(0.5)
# Das Programm wird mit Strg + C beendet

