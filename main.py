import sys
from datetime import datetime
import sqlite3 ## Wird verwendet um die Sensordaten in die SQLite-Datenbank zu speichern
import mysql.connector ## Wird verwendet um die Sensordaten in die MySQL-Datenbank zu speichern
import re ## Wird verwendet um reguläre Ausdrücke zu verwenden

datum = datetime.now() ## Aktuelles Datum
datum_als_long = int(datum.strftime("%Y%m%d%H%M%S")) ## Aktuelles Datum als long-Wert

def long_zu_zahl(datum_als_long): ## long-Wert in Zahl umwandeln
    return int(str(datum_als_long)[:8]) ## long-Wert in Zahl umwandeln

def parse_sensor_data(data):
    # Regex mit Vorzeichen und Sensorbezeichnung "Txx"
    pattern = r"(T\d{2})([+-])(\d+\.\d+)"
    matches = re.findall(pattern, data)

    sensor_values = []
    for sensor_id, sign, value in matches:
        sensor_entry = {
            "sensor_id": sensor_id,
            "sign": sign,
            "value": value
        }
        sensor_values.append(sensor_entry)

    return sensor_values



def save_to_mariadb(current_date, sensor_data): ## Sensordaten in MySQL-Datenbank speichern
    ip = "10.10.75.98" ## IP-Adresse des MySQL-Servers
    port = 3306 ## Port des MySQL-Servers
    user = "jgiera"
    password = "IBvm0-6BT7bxApKC" ## Passwort des MySQL-Nutzers
    dbname = "WerteDB" ## Name der Datenbank

    try:
        conn = mysql.connector.connect(host=ip, port=port, user=user, password=password, database=dbname) ## Verbindung zur MySQL-Datenbank herstellen
        cursor = conn.cursor()

        ## Daten in die Tabelle messung einfügen
        sensor_name = sensor_data["sensor_id"] ## Sensorname zusammensetzen
        cursor.execute('''
            INSERT INTO messung (datum, sensorName, Wert)
            VALUES (%s, %s, %s)
        ''', (current_date, sensor_name, sensor_data["value"])) ## Daten in die Tabelle messung einfügen

        conn.commit() ## Änderungen speichern
       # print("Sensordaten wurden erfolgreich in die MariaDB Datenbank gepseichert") ## Erfolgsmeldung
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() ## Verbindung schließen

def save_sensor_data(current_date, sensor_data): ## Sensordaten in SQLite-Datenbank speichern
    conn = sqlite3.connect('sensordaten.db') ## Verbindung zur SQLite-Datenbank herstellen
    cursor = conn.cursor()

    ## Datetime-Objekte in SQLite-Datenbank speichern
    sqlite3.register_adapter(datetime, lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"))

    ## Daten in die Tabelle messung einfügen
    sensor_name = sensor_data["sensor_id"] ## Sensorname zusammensetzen
    cursor.execute('''
        INSERT INTO messung (datum, sensorName, Wert)
        VALUES (?, ?, ?)
    ''', (current_date, sensor_name, sensor_data["value"])) ## Daten in die Tabelle messung einfügen

    conn.commit() ## Änderungen speichern
    conn.close() ## Verbindung schließen

if __name__ == "__main__": 
    if len(sys.argv) != 2: ## Fehlermeldung, wenn Sensordaten fehlen bzw kein Übergabeparameter vorhanden ist
        print("Bitte starte das Programm folgendermaßen: python main.py <sensor_data>")
        sys.exit(1)

    sensor_data = sys.argv[1] ## Sensordaten
    print(f"Hallo:_ {sensor_data}")

    sensor_data = parse_sensor_data(sensor_data) ## Sensordaten parsen
    
    for sensor_entry in sensor_data:
        print(f"Sensor {sensor_entry['sensor_id']}: Vorzeichen = {sensor_entry['sign']}, Wert = {sensor_entry['value']}")

        save_sensor_data(datum, sensor_entry) ## Sensordaten in SQLite-Datenbank speichern
        save_to_mariadb(datum, sensor_entry) ## Sensordaten in MySQL-Datenbank speichern



    print("Datum:", datum) ## Aktuelles Datum
    print("Datum als long:", datum_als_long) ## Aktuelles Datum als long-Wert

    print("Datum als Zahl:", long_zu_zahl(datum_als_long)) ## long-Wert in Zahl umwandeln

    print("Sensordaten wurden erfolgreich in die lokale SQLite-Datenbank gespeichert sowie auch beim MariaDB Server.") ## Erfolgsmeldung

