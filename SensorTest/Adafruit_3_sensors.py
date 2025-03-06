import Adafruit_ADS1x15
import time

#A0 -> LDR
#A1 -> Potentiometer
#A2 -> PTC


adc = Adafruit_ADS1x15.ADS1115(busnum=1) # Wird auf Bus 1 initialisiert
GAIN = 1 # Verstärkung des ADCs
DATA_RATE = 860  # Maximale Datenrate für schnellere Konversionen

while True:
    value1 = adc.read_adc(0, gain=GAIN, data_rate=DATA_RATE) #Wert des LDRs wird ausgelesen
    value2 = adc.read_adc(1, gain=GAIN, data_rate=DATA_RATE) #Wert des Potentiometers wird ausgelesen
    value3 = adc.read_adc(2, gain=GAIN, data_rate=DATA_RATE) #Wert des PTCs wird ausgelesen

    print("LDR: {0:>6}".format(value1) + "Poti: {0:>6}".format(value2) + "PTC: {0:>6}".format(value3))
    time.sleep(0.5)
# Das Programm wird mit Strg + C beendet

