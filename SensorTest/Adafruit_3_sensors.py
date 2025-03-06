import Adafruit_ADS1x15
import time

#A0 -> Potentiometer
#A1 -> LDR
#A2 -> PTC


adc = Adafruit_ADS1x15.ADS1115(busnum=1) # Wird auf Bus 1 initialisiert
GAIN = 1 # Verstärkung des ADCs
DATA_RATE = 860  # Maximale Datenrate für schnellere Konversionen

while True:
    value1 = adc.read_adc(0, gain=GAIN, data_rate=DATA_RATE) #Wert des LDRs wird ausgelesen
    value2 = adc.read_adc(1, gain=GAIN, data_rate=DATA_RATE) #Wert des Potentiometers wird ausgelesen
    value3 = adc.read_adc(2, gain=GAIN, data_rate=DATA_RATE) #Wert des PTCs wird ausgelesen

    print("Poti: {0:>6} | LDR: {1:>6} | NTC: {2:>6}".format(value1, value2, value3))
    time.sleep(0.5)
# Das Programm wird mit Strg + C beendet

