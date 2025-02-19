#Testen deer Messung eines Potentiometers mit einem Raspberry Pi.
# Der Wandler ADS1115 wird verwendet.

#Pinbelegung:
#VDD -> pin 1
#GND -> pin 6
#SCL -> pin 5
#SDA -> pin 3

#A0 -> Mittlerer Pin des Potentiometers

import Adafruit_ADS1x15
import time

adc = Adafruit_ADS1x15.ADS1115(busnum=1) # Eine ADS1115 Instanz wird erstellt
GAIN = 1

while True:
    values = adc.read_adc(0, gain=GAIN) # Der Wert des Potentiometers wird ausgelesen
    print('{0:>6}'.format(values)) # Der Wert wird ausgegeben
    time.sleep(0.5) # Wartezeit von 0.5 Sekunden

#Das Programm wird mit Strg + C beendet


