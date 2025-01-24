import sys
from datetime import datetime

def parse_sensor_data(data): ## Sensordaten parsen
    start = data[0] ## Startzeichen
    sensor_type = data[1] ## Sensortyp
    sensor_number = data[2:4] ## Sensornummer
    sign = data[4] ## Vorzeichen
    value = data[5:-1] ## Wert
    end = data[-1] ## Endzeichen
    return start, sensor_type, sensor_number, sign, value, end ## Rückgabe der Sensordaten

if __name__ == "__main__": 
    if len(sys.argv) != 2: ## Fehlermeldung, wenn Sensordaten fehlen bzw kein Übergabeparameter vorhanden ist
        print("Bitte starte das Programm folgendermaßen: python main.py <sensor_data>")
        sys.exit(1)

    sensor_data = sys.argv[1] ## Sensordaten
    print(f"Hallo:_ {sensor_data}")

    start, sensor_type, sensor_number, sign, value, end = parse_sensor_data(sensor_data) ## Sensordaten parsen
    print(start)
    print(sensor_type)
    print(sensor_number)
    print(sign)
    print(value)
    print(end)

    current_date = datetime.now()
    print(current_date) ## Aktuelles Datum
    print(current_date.strftime("%Y%m%d")) ## Datum in Format JJJJMMTT
