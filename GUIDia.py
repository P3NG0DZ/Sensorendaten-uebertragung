#Programm was ein Liniendiagramm von den Messwerten aus der MariaDB Datenbank erstellt
# Man kann auswählen welchen SensorName man als Liniendiagramm haben möchte (Beispiel: T01, S01 etc)
# Die Werte werden Sortiert nach Datum und Uhrzeit (In Datumtabelle)

import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel, QVBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.dates import DateFormatter  # DateFormatter importieren

def connect_to_db(sensor_name=None): ## Verbindung zur MySQL-Datenbank
    ip = "10.10.75.98" ## IP-Adresse des MySQL-Servers
    port = 3306 ## Port des MySQL-Servers
    user = "jgiera"
    password = "IBvm0-6BT7bxApKC" ## Passwort des MySQL-Nutzers
    dbname = "WerteDB" ## Name der Datenbank

    try:
        conn = mysql.connector.connect(host=ip, port=port, user=user, password=password, database=dbname) ## Verbindung zur MySQL-Datenbank herstellen
        cursor = conn.cursor()

        if sensor_name:
            ## Daten aus der Tabelle messung abfragen
            cursor.execute('''
                SELECT datum, Wert
                FROM messung
                WHERE sensorName = %s
                ORDER BY datum
                LIMIT 1000  -- Begrenze die Anzahl der abgerufenen Zeilen zur Leistungsverbesserung
            ''', (sensor_name,)) ## Daten aus der Tabelle messung abfragen
        else:
            ## Alle SensorNamen abfragen
            cursor.execute('''
                SELECT DISTINCT sensorName
                FROM messung
            ''')
        
        data = cursor.fetchall()

        return data
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

class GUIDia(QWidget): ## Klasse für die GUI
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liniendiagramm")
        self.resize(1400, 900)  # Fenstergröße erhöhen

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.sensor_label = QLabel("Sensor:")
        self.layout.addWidget(self.sensor_label)

        self.sensor_combobox = QComboBox()
        self.layout.addWidget(self.sensor_combobox)

        self.plot_button = QPushButton("Diagramm anzeigen")
        self.plot_button.clicked.connect(self.plot)
        self.layout.addWidget(self.plot_button)

        self.plot_widget = plt.figure(figsize=(20, 20))  #
        self.plot_widget_canvas = FigureCanvas(self.plot_widget)
        self.layout.addWidget(self.plot_widget_canvas)

        self.init_combobox()

    def init_combobox(self): ## Combobox mit den SensorNamen füllen
        data = connect_to_db()
        sensor_names = set([x[0] for x in data])

        for sensor_name in sensor_names:
            self.sensor_combobox.addItem(sensor_name)

    def plot(self): ## Liniendiagramm erstellen
        sensor_name = self.sensor_combobox.currentText()
        data = connect_to_db(sensor_name)

        df = pd.DataFrame(data, columns=["Datum", "Wert"])
        df["Datum"] = pd.to_datetime(df["Datum"])
        df["Wert"] = pd.to_numeric(df["Wert"], errors='coerce')  # "Wert" in numerisch umwandeln

        self.plot_widget.clear()  # Plot leeren
        ax = self.plot_widget.add_subplot(111)
        ax.clear()
        ax.plot(df["Datum"], df["Wert"], marker='o')  # Erkennungszeichen für die Datenpunkte
        ax.set_title(f"Liniendiagramm für Sensor {sensor_name}")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Wert")
        ax.grid(True)
        ax.xaxis.set_major_formatter(DateFormatter('%d.%m.%Y %H:%M Uhr'))  # Datumsformat für x-Achse

        # Setze x-Ticks nur an eindeutigen Datenpunkten und vermeide Überlappungen
        unique_dates = df["Datum"].unique()
        if len(unique_dates) > 10:  # Schwellenwert nach Bedarf anpassen
            ax.set_xticks(unique_dates[::len(unique_dates)//10])
        else:
            ax.set_xticks(unique_dates)
        
        plt.xticks(rotation=45, fontsize=8, ha='right')  # Drehe Datumsbeschriftungen für bessere Lesbarkeit und reduziere Schriftgröße

        # Füge einen kleinen Rand zu den y-Achsen-Grenzen hinzu
        y_min = df["Wert"].min()
        y_max = df["Wert"].max()
        if y_min == y_max:
            y_min -= 1
            y_max += 1
        ax.set_ylim(y_min, y_max)

        self.plot_widget_canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUIDia()
    window.show()
    sys.exit(app.exec_())


