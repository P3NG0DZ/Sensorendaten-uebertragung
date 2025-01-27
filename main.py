import sys
from datetime import datetime
import sqlite3 ## Wird verwendet um die Sensordaten in die SQLite-Datenbank zu speichern
datum = datetime.now() ## Aktuelles Datum
datum_als_long = int(datum.strftime("%Y%m%d%H%M%S")) ## Aktuelles Datum als long-Wert

def long_zu_zahl(datum_als_long): ## long-Wert in Zahl umwandeln
    return int(str(datum_als_long)[:8]) ## long-Wert in Zahl umwandeln



def parse_sensor_data(data): ## Sensordaten parsen
    start = data[0] ## Startzeichen
    sensor_type = data[1] ## Sensortyp
    sensor_number = data[2:4] ## Sensornummer
    sign = data[4] ## Vorzeichen
    value = data[5:-1] ## Wert
    end = data[-1] ## Endzeichen
    return start, sensor_type, sensor_number, sign, value, end ## Rückgabe der Sensordaten

def save_sensor_data(current_date, sensor_data): ## Sensordaten in SQLite-Datenbank speichern
    conn = sqlite3.connect('sensordaten.db') ## Verbindung zur SQLite-Datenbank herstellen
    cursor = conn.cursor()

    ## Datetime-Objekte in SQLite-Datenbank speichern
    sqlite3.register_adapter(datetime, lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"))

    ## Daten in die Tabelle messung einfügen
    sensor_name = f"{sensor_data[1]}{sensor_data[2:4]}" ## Sensorname zusammensetzen
    cursor.execute('''
        INSERT INTO messung (datum, sensorName, Wert)
        VALUES (?, ?, ?)
    ''', (current_date, sensor_name, sensor_data[4])) ## Daten in die Tabelle messung einfügen

    conn.commit() ## Änderungen speichern
    conn.close() ## Verbindung schließen

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

    print("Datum:", datum) ## Aktuelles Datum
    print("Datum als long:", datum_als_long) ## Aktuelles Datum als long-Wert

    print("Datum als Zahl:", long_zu_zahl(datum_als_long)) ## long-Wert in Zahl umwandeln


    print("Speichern der Sensordaten in die SQLite-Datenbank...")
    save_sensor_data(datum, sensor_data)
    


    print("Sensordaten wurden erfolgreich in die SQLite-Datenbank gespeichert.") ## Erfolgsmeldung
