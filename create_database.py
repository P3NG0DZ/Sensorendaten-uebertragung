import sqlite3

def create_database():
    conn = sqlite3.connect('sensordaten.db')  # Verbindung zur SQLite-Datenbank herstellen
    cursor = conn.cursor()

    # Tabelle erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messung (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT,
            sensorName TEXT,
            Wert TEXT
        )
    ''')

    conn.commit()  # Änderungen speichern
    conn.close()  # Verbindung schließen

if __name__ == "__main__":
    create_database()
    print("Datenbank und Tabelle wurden erfolgreich erstellt.")
