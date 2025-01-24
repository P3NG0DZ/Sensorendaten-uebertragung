import sqlite3

def create_database():
    conn = sqlite3.connect('sensordaten.db')  # Verbindung zur SQLite-Datenbank herstellen
    cursor = conn.cursor()

    # Tabelle erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensordaten (
            id INTEGER PRIMARY KEY,
            komplett TEXT,
            startzeichen TEXT,
            sensortyp TEXT,
            sensornummer TEXT,
            vorzeichen TEXT,
            wert REAL,
            endzeichen TEXT,
            datum TEXT,
            datum_als_zahl TEXT
        )
    ''')

    conn.commit()  # Änderungen speichern
    conn.close()  # Verbindung schließen

if __name__ == "__main__":
    create_database()
    print("Datenbank und Tabelle wurden erfolgreich erstellt.")
