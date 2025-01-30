## Datenübertragung

Dieses Projekt wird sich darauf beziehen, Sensorenübertragung durchzuführen. Auch wird sich mit dem Auswerten eines Strings beschäftigt.

Es handelt sich hierbei um ein Schulprojekt. Nichts spannendes. Wer gerne meinen Weg verfolgen will oder so ein ähnliches Projekt hat, fühlt euch frei, diesen Code etwas zu verändern oder zu nutzen :)

Diese Werte werden dann in einer Datenbank angelegt (Lokal so als auch auf einem Server).

## Der Plan (Protokoll zur Sensordatenübertragung)

:T00+000.1;      wobei

: = Startzeichen  
T = Art des Sensors  
00 = Nummer des Sensors  
"+" = Vorzeichen  
000.0 = Stellenanzahl  
; = Abschlusszeichen  

Das Programm soll mithilfe eines Übergabeparameters gestartet werden.  
Beispiel: `python main.py ":T01+015.1;"`

Der Code soll dann zuerst folgendes ausgeben:
1. Hallo:_ :T01+015.1;
2. :
3. T
4. 01
5. "+"
6. 015.1
7. ;
8. Datum
9. Datum als long

Die Zeit soll sowohl im normalen Format als auch als Long-Wert ausgegeben werden. Der Long-Wert wird anschließend wieder in ein Datum umgewandelt.

Es wurde extra ein MariaDB-Server aufgesetzt, um die Sensordaten in einer Datenbank zu speichern. Genutzt wird hier eine Raspberry Pi 3b+.
Bis jetzt wird sie auch noch lokal gespeichert. Eine Anleitung wie man ein MariaDB-Server mit phpMyAdmin aufsetzt, findet ihr bei diesem Markdown:
Installation phpmyadmin mit MariaDB Linux

Zudem soll es auch möglich sein, dass es einen komplexen Eingabestring verarbeiten kann.

Beispiel: `:T00+001.0T01+002.0T02+003.0T03+010.0T04+011.0T05+012.0T06+010.0T07+011.0T08+012.0;`
Der Eingabestring erhält mehrere Sensordaten, die nacheinander verarbeitet werden sollen.

## Erklärung des Python Codes:

### parse_sensor_data(data)
Diese Funktion nimmt einen String `data` im Sensordatenformat und zerlegt ihn in seine Bestandteile:
- `sensor_art`: Art des Sensors (z.B. T)
- `sensor_nummer`: Nummer des Sensors (z.B. 01)
- `sign`: Vorzeichen des Wertes (z.B. +)
- `value`: Wert des Sensors (z.B. 015.1)

### long_zu_zahl(datum_als_long)
Diese Funktion wandelt einen Long-Wert in eine Zahl um, indem sie die ersten acht Ziffern des Long-Werts extrahiert.

### save_to_mariadb(current_date, sensor_data)
Diese Funktion speichert die Sensordaten in einer MariaDB Datenbank. Sie stellt eine Verbindung zur Datenbank her, fügt die Daten in die Tabelle `messung` ein und schließt die Verbindung.

### save_sensor_data(current_date, sensor_data)
Diese Funktion speichert die Sensordaten in einer lokalen SQLite-Datenbank. Sie stellt eine Verbindung zur Datenbank her, fügt die Daten in die Tabelle `messung` ein und schließt die Verbindung.

### Hauptprogramm
Das Hauptprogramm führt folgende Schritte aus:
1. Überprüft, ob das Programm mit genau einem Parameter gestartet wurde.
2. Gibt den übergebenen Sensordaten-String aus.
3. Zerlegt den Sensordaten-String in seine Bestandteile und gibt diese aus.
4. Gibt das aktuelle Datum, das Datum als Long-Wert und das umgewandelte Datum zurück.
5. Speichert die Sensordaten in einer lokalen SQLite-Datenbank und auf einem MariaDB-Server.


## Installation von MariaDB und phpMyAdmin unter Linux

Diese Anleitung beschreibt die Schritte zur Installation von MariaDB und phpMyAdmin unter Linux sowie die Einrichtung einer Datenbank. Diese Anleitung umfasst auch die Konfiguration für den Fernzugriff.

### Voraussetzungen

- Ein Linux-System mit Root-Zugriff
- Ein Terminal

### Schritt 1: MariaDB installieren

1. Öffne ein Terminal.
2. Aktualisiere die Paketliste:
    ```bash
    sudo apt update
    ```
3. Installiere MariaDB:
    ```bash
    sudo apt install mariadb-server
    ```
4. Starte den MariaDB-Dienst und aktiviere ihn beim Systemstart:
    ```bash
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    ```
5. Führe das Sicherheits-Skript aus, um die Installation abzusichern:
    ```bash
    sudo mysql_secure_installation
    ```
    Folge den Anweisungen auf dem Bildschirm.

### Schritt 2: phpMyAdmin installieren

1. Installiere phpMyAdmin:
    ```bash
    sudo apt install phpmyadmin
    ```
2. Wähle während der Installation den Webserver aus (z.B. Apache2) und konfiguriere die Datenbank für phpMyAdmin.

### Schritt 3: MariaDB konfigurieren

1. Melde dich bei MariaDB an:
    ```bash
    sudo mysql -u root -p
    ```
2. Erstelle eine neue Datenbank:
    ```sql
    CREATE DATABASE WerteDB;
    ```
3. Erstelle einen neuen Benutzer und gewähre ihm alle Rechte auf die neue Datenbank:
    ```sql
    CREATE USER 'benutzer'@'%' IDENTIFIED BY 'passwort';
    GRANT ALL PRIVILEGES ON WerteDB.* TO 'benutzer'@'%';
    FLUSH PRIVILEGES;
    ```
4. Beende die MariaDB-Sitzung:
    ```sql
    EXIT;
    ```

### Schritt 4: MariaDB für Fernzugriff konfigurieren

1. Öffne die MariaDB-Konfigurationsdatei:
    ```bash
    sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
    ```
2. Suche die Zeile mit `bind-address` und ändere sie auf `0.0.0.0`:
    ```ini
    bind-address = 0.0.0.0
    ```
3. Speichere die Datei und starte den MariaDB-Dienst neu:
    ```bash
    sudo systemctl restart mariadb
    ```

### Schritt 5: Firewall konfigurieren

1. Erlaube den Fernzugriff auf den MariaDB-Port (3306):
    ```bash
    sudo ufw allow 3306/tcp
    ```

### Schritt 6: phpMyAdmin konfigurieren

1. Öffne deinen Webbrowser und navigiere zu `http://<deine-ip-adresse>/phpmyadmin`.
2. Melde dich mit dem neu erstellten Benutzer `benutzer` und dem Passwort `passwort` an.
3. Wähle die Datenbank `WerteDB` aus und erstelle die Tabelle `messung`:
    ```sql
    CREATE TABLE messung (
        id INT AUTO_INCREMENT PRIMARY KEY,
        datum TEXT,
        sensorName TEXT,
        Wert TEXT
    );
    ```

### Schritt 7: Datenbank in phpMyAdmin erstellen

1. Melde dich bei phpMyAdmin an, indem du `http://<deine-ip-adresse>/phpmyadmin` in deinem Webbrowser aufrufst.
2. Gib den Benutzernamen `root` und das Passwort ein, das du während der MariaDB-Installation festgelegt hast.
3. Klicke auf "Datenbanken" im oberen Menü.
4. Gib unter "Datenbank erstellen" den Namen `WerteDB` ein und klicke auf "Anlegen".
5. Wähle die neu erstellte Datenbank `WerteDB` aus der Liste auf der linken Seite aus.
6. Klicke auf "SQL" im oberen Menü und füge das folgende SQL-Skript ein, um die Tabelle `messung` zu erstellen:
    ```sql
    CREATE TABLE messung (
        id INT AUTO_INCREMENT PRIMARY KEY,
        datum TEXT,
        sensorName TEXT,
        Wert TEXT
    );
    ```
7. Klicke auf "OK", um das Skript auszuführen und die Tabelle zu erstellen.

### Fertig!

Du hast nun MariaDB und phpMyAdmin installiert und eine Datenbank eingerichtet. Du kannst nun Sensordaten in die Datenbank speichern und verwalten und von anderen Geräten aus darauf zugreifen.


