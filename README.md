# Sensordatenübertragung

Dieses Projekt befasst sich mit der Erfassung, Übertragung und Speicherung von Sensordaten. Die Daten werden sowohl lokal als auch auf einem Server gespeichert und können über eine grafische Benutzeroberfläche visualisiert werden.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Sensordatenformat](#sensordatenformat)
- [Funktionalität](#funktionalität)
- [Installation & Einrichtung](#installation--einrichtung)
- [Verwendung](#verwendung)
- [Datenbankintegration](#datenbankintegration)
- [GUI-Datenvisualisierung](#gui-datenvisualisierung)
- [Automatisierte Datenübertragung](#automatisierte-datenübertragung)
- [Anwendungsbeispiel](#Anwendungsbeispiel)
- [Webserver](#webserver)
- [Lizenz](#lizenz)
  
  

## Überblick

Das Projekt ermöglicht die Übertragung von Sensordaten über eine serielle Schnittstelle oder per Dateiimport. Die Daten werden analysiert, gespeichert und können über verschiedene Schnittstellen weiterverarbeitet werden.

## Sensordatenformat

Die Sensordaten folgen einem standardisierten Format:

```plaintext
:T00+000.1;
```

**Bedeutung der Komponenten:**

| Zeichen | Bedeutung        |
| ------- | ---------------- |
| `:`     | Startzeichen     |
| `T`     | Sensortyp        |
| `00`    | Sensor-ID        |
| `+`     | Vorzeichen       |
| `000.1` | Messwert         |
| `;`     | Abschlusszeichen |

## Funktionalität

- **Echtzeit-Datenverarbeitung** über serielle Schnittstelle
- **Speicherung** der Messwerte in SQLite und MariaDB
- **CSV-Export** zur Weiterverarbeitung
- **Grafische Visualisierung** der Messwerte mit Matplotlib oder bei SensorDia.java mit JFreeChart

## Installation & Einrichtung

### Voraussetzungen

- Raspberry Pi 3b+ (oder kompatibles System)
- Python 3 mit erforderlichen Bibliotheken
- MariaDB-Server für serverseitige Speicherung

### Installation

```bash
sudo apt update && sudo apt install -y python3 python3-pip mariadb-server
pip3 install -r requirements.txt
```

## Verwendung

### Start des Programms

Das Hauptskript wird mit einem Sensordaten-String als Parameter gestartet:

```bash
python main.py ":T01+015.1;"
```

Die Ausgabe enthält:

1. Den Original-String
2. Zerlegte Werte (Sensortyp, ID, Vorzeichen, Wert)
3. Zeitstempel (normal und als Unix-Timestamp)
4. Speicherung der Werte in Datenbanken und CSV

## Datenbankintegration

**MariaDB-Setup:**

```sql
CREATE DATABASE WerteDB;
CREATE TABLE messwerte (
    id INTEGER PRIMARY KEY,
    datum TEXT,
    sensorName TEXT,
    Wert TEXT
);
```

## GUI-Datenvisualisierung

Eine GUI-Anwendung erlaubt die Auswahl eines Sensors und zeigt dessen Messwerte als Diagramm.

### Starten der GUI

```bash
python GUIDia.py
```

## Automatisierte Datenübertragung

Ein Bash-Skript `transfer.sh` kann Sensordaten automatisch an einen Server senden.

```bash
./transfer.sh
```

## Anwendungsbeispiel

### Voraussetzungen

- 1x Raspberry Pi 3B+
- 1x ADS1115
- 3x 10KOhm Widerstände (1x Pro Komponente)
- 1x Potentiometer
- 1x LDR
- 1x NTC

### Schaltplan

Wenn ihr einen ADS1115 Mikrocontroller habt, könnt ihr Sensorwerte z.B. von einem Potentiometer, einem PTC (Kaltleiter) oder einem LDR (Fotowiderstand) einlesen. Die Codes können frei geändert werden. Updates folgen

![SensorTest](SensorTest/#^files)

Um den Code auf dem Pi zu implementieren, folgen Sie diesem Schaltplan.

Belegung von den Microcontroller:

- A0: Potentiometer
- A1: LDR
- A2: NTC

![Schaltplan](Plaene/Schaltplan.png)
![Steckplan](Plaene/Steckplan.png)

## Webserver

Der Webserver stellt die grafische Oberfläche zur Echtzeit-Visualisierung der Sensordaten (über die Datei index.html) bereit und liefert über sensordata.php einen API-Endpunkt für den Datenabruf.



Um den Webserver selber zu Installieren benötigt man nginx. Dies kann man einfach mit 

```bash
sudo apt install nginx
```

installieren. Zudem wird auch nochmal PHP benötigt. Diese installiert man mit

```bash
sudo apt install php php-fpm
```

### Falls Apache installiert

Damit kein Konflikt mit Apache entsetht und auch richtig mit php läuft wird der Port auf 8001 gesetzt und fügen php hinzu. Die Config befindet sich in der Repository unter **Webserver/config**. Bitte beachtet, dass wenn es Updates von php gibt oder ähnliche Updates die Kofigurationsdatei manuell angepasst werden muss. Der Stand der Config Datei ist der 2. April. 2025. Wenn ihr kein Apache benötigt, Apache nicht installiert habt oder letzendlich Apache etnfernt, könnt ihr den Port standardmäßig auf 80 lassen (Änderung an der Repo Config nötig) solange der Port nicht von was anderes belegt wird. 

Sucht einfach unter der Config nach <mark>listen</mark> und ändert die beiden Ports entweder zu 80 oder zu einem beliebigen Port deiner Wahl.



### Geänderte Config übertragen

Füge das an einen beliebigen Verzeichnis der Raspberry Pi hinzu und öffne das Terminal. Gebe folgendes ein 



```bash
cd /etc/nginx-sites-available/ #Navigiert zum Verzeichnis der Config
```

```bash
sudo cp default /dein-verzeichnis #Aender dein-verzeichnis zu einem beliebigen Verzeichnis. Dient zum Backup

```

```bash
sudo rm default #Entfernt die Config aus dem Verzeichnis

```

```bash
sudo cp /config-verzeichnis/default /etc/nginx-sites-available/
#Aender config-verzeichnis/default zu dem Verzeichnis, wo du die modifizierte Config gespeichert hast
```

Der Webserver muss nun gestartet werden und in den Autostart aufgenommen werden mit:

```bash
sudo systemctl start php8.2-fpm
sudo systemctl start nginx

sudo systemctl enable php8.2-fpm
sudo systemctl enable nginx 
```

Probiere die nginx default Seite mit

```
http://<RaspberryIP>:<Port>
```

Lass den Portabschnitt leer (Ab dem Doppelpunkt) wenn der Port in der Config 80 ist



Falls da was kommt ist der WebServer Konfiguriert.

## Lizenz

 ![LICENSE](LICENSE.md)

## 
