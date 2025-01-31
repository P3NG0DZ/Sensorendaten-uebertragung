import sys
import csv
from datetime import datetime
import sqlite3 ## Wird verwendet um die Sensordaten in die SQLite-Datenbank zu speichern
import mysql.connector ## Wird verwendet um die Sensordaten in die MySQL-Datenbank zu speichern
import re ## Wird verwendet um reguläre Ausdrücke zu verwenden

datum = datetime.now() ## Aktuelles Datum
datum_als_long = int(datum.strftime("%Y%m%d%H%M%S")) ## Aktuelles Datum als long-Wert

def long_zu_zahl(datum_als_long): ## long-Wert in Zahl umwandeln
    return int(str(datum_als_long)[:8]) ## long-Wert in Zahl umwandeln

def parse_sensor_data(data):
    # Regex, um T (Sensorart), Nummer (zwei Ziffern), Vorzeichen und Wert zu extrahieren
    pattern = r"(T)(\d{2})([+-])(\d+\.\d+)"
    matches = re.findall(pattern, data)

    sensor_values = []
    for sensor_art, sensor_nummer, sign, value in matches:
        sensor_entry = {
            "sensor_art": sensor_art,
            "sensor_nummer": sensor_nummer,
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
        sensor_name = f"{sensor_data['sensor_art']}{sensor_data['sensor_nummer']}" ## Sensorname zusammensetzen
        cursor.execute('''
            INSERT INTO messung (datum, sensorName, Wert)
            VALUES (%s, %s, %s)
        ''', (current_date.strftime('%Y-%m-%d %H:%M:%S'), sensor_name, sensor_data["value"])) ## Daten in die Tabelle messung einfügen

        conn.commit() ## Änderungen speichern
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
    sqlite3.register_adapter(datetime, lambda dt: dt.timestamp())

    ## Daten in die Tabelle messung einfügen
    sensor_name = f"{sensor_data['sensor_art']}{sensor_data['sensor_nummer']}" ## Sensorname zusammensetzen
    cursor.execute('''
        INSERT INTO messung (datum, sensorName, Wert)
        VALUES (?, ?, ?)
    ''', (current_date.strftime('%Y-%m-%d %H:%M:%S'), sensor_name, sensor_data["value"])) ## Daten in die Tabelle messung einfügen

    conn.commit() ## Änderungen speichern
    conn.close() ## Verbindung schließen

def write_to_csv(data): ## Sensordaten in CSV-Datei speichern. Jeder Datensatz bekommt eine eigene Zeile
    file_exists = False
    try:
        with open('messdaten.csv', mode='r', newline='') as file: ## Überprüfen ob die Datei bereits existiert
            file_exists = True
    except FileNotFoundError:
        pass

    with open('messdaten.csv', mode='a', newline='') as file: ## Sensordaten in CSV-Datei speichern
        writer = csv.writer(file) ## CSV-Writer erstellen
        if not file_exists:
            writer.writerow(["Datum", "SensorName", "Wert"])
        for sensor_entry in data:
            sensor_name = f"{sensor_entry['sensor_art']}{sensor_entry['sensor_nummer']}"
            writer.writerow([datum.strftime('%Y-%m-%d %H:%M:%S'), sensor_name, sensor_entry["value"]])

if __name__ == "__main__": 
    if len(sys.argv) != 2: ## Fehlermeldung, wenn Sensordaten fehlen bzw kein Übergabeparameter vorhanden ist
        print("Bitte starte das Programm folgendermaßen: python main.py <sensor_data>")
        sys.exit(1)

    sensor_data = sys.argv[1] ## Sensordaten
    print(f"Hallo:_ {sensor_data}")

    sensor_data = parse_sensor_data(sensor_data) ## Sensordaten parsen
    
    for sensor_entry in sensor_data:
        print(f"Sensorart = {sensor_entry['sensor_art']}, Sensor Nummer = {sensor_entry['sensor_nummer']}, Vorzeichen = {sensor_entry['sign']}, Wert = {sensor_entry['value']}")
        save_sensor_data(datum, sensor_entry) ## Sensordaten in SQLite-Datenbank speichern
        try:
            save_to_mariadb(datum, sensor_entry) ## Sensordaten in MySQL-Datenbank speichern
        except Exception as e:
            print(f"Fehler beim Speichern in MariaDB")
            print("Überspringe das Speichern in MariaDB und fahre fort.")

        write_to_csv([sensor_entry]) ## Sensordaten in CSV-Datei speichern



    print("Datum:", datum) ## Aktuelles Datum
    print("Datum als long:", datum_als_long) ## Aktuelles Datum als long-Wert

    print("Datum als Zahl:", long_zu_zahl(datum_als_long)) ## long-Wert in Zahl umwandeln

    print("Sensordaten wurden erfolgreich gespeichert") ## Erfolgsmeldung

