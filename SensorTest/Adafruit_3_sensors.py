import Adafruit_ADS1x15
import time

adc = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1
DATA_RATE = 860  # Maximale Datenrate für schnellere Konversionen

def get_avg(channel, samples=100):
    # Starte den kontinuierlichen Modus für den gewünschten Kanal
    adc.start_adc(channel, gain=GAIN, data_rate=DATA_RATE)
    # Kurze Wartezeit, damit der erste Messwert vorliegt
    time.sleep(1.0 / DATA_RATE)
    values = []
    for _ in range(samples):
        value = adc.get_last_result()
        values.append(value)
        # Warten, bis der nächste Messwert verfügbar ist
        time.sleep(1.0 / DATA_RATE)
    adc.stop_adc()
    return sum(values) / len(values)

while True:
    # Kanäle nacheinander abfragen
    avg_poti = get_avg(0)
    avg_ldr  = get_avg(1)
    avg_ptc  = get_avg(2)
    
    print("Messung: LDR: {}  Poti: {}  PTC: {}".format(avg_ldr, avg_poti, avg_ptc))
    
    time.sleep(0.5)
