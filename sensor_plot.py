# Programm zum Erstellen von Liniendiagrammen aus CSV-Daten
import matplotlib.pyplot as plt
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLabel, QVBoxLayout, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore import Qt
from matplotlib.dates import DateFormatter, AutoDateLocator
import argparse
import matplotlib.dates as mdates

def read_csv(file_path, sensor_name=None):
    try:
        df = pd.read_csv(file_path)
        df = df.dropna(subset=["Datum"])  # Leerzeilen entfernen
        
        if "Vorzeichen" in df.columns:
            # Vorzeichen in numerische Werte umwandeln
            df["Vorzeichen"] = df["Vorzeichen"].map({'+': 1, '-': -1})
            df["Wert"] = df["Vorzeichen"] * pd.to_numeric(df["Wert"], errors='coerce')
        else:
            df["Wert"] = pd.to_numeric(df["Wert"], errors='coerce')
        
        # Datum in datetime umwandeln, falls es als String vorliegt
        if df["Datum"].dtype == 'object':
            df["Datum"] = pd.to_datetime(df["Datum"], format='%Y-%m-%d %H:%M:%S')
        
        if sensor_name:
            df = df[df["SensorName"] == sensor_name]
        
        return df.sort_values("Datum")
    except Exception as e:
        print(f"Fehler beim Lesen der CSV-Datei: {e}")
        sys.exit(1)

class GUIDia(QWidget):
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file
        self.setWindowTitle("Liniendiagramm")
        self.resize(2000, 1500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # GUI-Elemente
        self.sensor_label = QLabel("Sensor:")
        self.layout.addWidget(self.sensor_label)

        self.sensor_combobox = QComboBox()
        self.sensor_combobox.currentIndexChanged.connect(self.plot)
        self.layout.addWidget(self.sensor_combobox)

        self.toggle_checkbox = QCheckBox("Alle Sensoren anzeigen")
        self.toggle_checkbox.stateChanged.connect(self.toggle_sensor_selection)
        self.layout.addWidget(self.toggle_checkbox)

        # Matplotlib Figure
        self.plot_widget = plt.figure(figsize=(30, 15))
        self.plot_widget_canvas = FigureCanvas(self.plot_widget)
        self.layout.addWidget(self.plot_widget_canvas)

        self.init_combobox()
        self.plot()  # Initialer Plot

    def init_combobox(self):
        df = read_csv(self.csv_file)
        self.sensor_combobox.clear()
        self.sensor_combobox.addItems(sorted(df["SensorName"].unique()))

    def toggle_sensor_selection(self):
        self.sensor_combobox.setEnabled(not self.toggle_checkbox.isChecked())
        self.plot()

    def plot(self):
        show_all_sensors = self.toggle_checkbox.isChecked()
        sensor_name = None if show_all_sensors else self.sensor_combobox.currentText()

        # Daten laden
        df = read_csv(self.csv_file, sensor_name=sensor_name)

        # Plot zurücksetzen
        self.plot_widget.clear()
        ax = self.plot_widget.add_subplot(111)
        ax.clear()

        # Farbpalette für Sensoren
        colors = plt.cm.tab20.colors  # Verwende die "tab20"-Farbpalette
        sensor_names = df["SensorName"].unique()
        color_map = {name: colors[i % len(colors)] for i, name in enumerate(sensor_names)}

        # Plot-Logik
        if show_all_sensors:
            # Plot ALLE Sensoren mit unterschiedlichen Farben
            for name, group in df.groupby("SensorName"):
                if len(group) == 1:
                    # Füge einen zweiten Datenpunkt hinzu, um eine Linie zu zeichnen
                    group = pd.concat([group, group])
                ax.plot(group["Datum"], group["Wert"], '-', markersize=4, linewidth=1, label=name, color=color_map[name])
        else:
            # Plot einzelner Sensor
            if not df.empty:
                if len(df) == 1:
                    # Füge einen zweiten Datenpunkt hinzu, um eine Linie zu zeichnen
                    df = pd.concat([df, df])
                ax.plot(df["Datum"], df["Wert"], '-o', markersize=4, linewidth=1, label=sensor_name, color=color_map[sensor_name])

        # Achsenformatierung
        ax.set_title("Sensorwerte", fontsize=14, pad=20)
        ax.set_xlabel("Datum", fontsize=12)
        ax.set_ylabel("Wert", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Datumsformatierung
        ax.xaxis.set_major_locator(AutoDateLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%d.%m.%Y %H:%M'))
        plt.xticks(fontsize=9, rotation=45, ha='right')
        plt.gcf().autofmt_xdate()

        # Y-Achsen Puffer
        if not df.empty:
            y_min, y_max = df["Wert"].agg(['min', 'max'])
            y_range = y_max - y_min
            ax.set_ylim(y_min - y_range*0.1, y_max + y_range*0.1)

        # Legende
        if not df.empty:
            legend = ax.legend(
                loc='upper center',
                bbox_to_anchor=(0.5, -0.25),
                ncol=8,
                fontsize='xx-small',
                columnspacing=1,
                frameon=False
            )

        # Layoutoptimierung
        plt.subplots_adjust(
            left=0.05,
            right=0.95,
            bottom=0.3,
            top=0.95,
            hspace=0.4
        )
        
        self.plot_widget_canvas.draw()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="Pfad zur CSV-Datei")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = GUIDia(args.csv_file)
    window.show()
    sys.exit(app.exec_())