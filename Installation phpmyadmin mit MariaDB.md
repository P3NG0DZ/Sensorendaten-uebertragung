# Installation von MariaDB und phpMyAdmin unter Linux

Diese Anleitung beschreibt die Schritte zur Installation von MariaDB und phpMyAdmin unter Linux sowie die Einrichtung einer Datenbank. Diese Anleitung umfasst auch die Konfiguration für den Fernzugriff.

## Voraussetzungen

- Ein Linux-System mit Root-Zugriff
- Ein Terminal

## Schritt 1: MariaDB installieren

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

## Schritt 2: phpMyAdmin installieren

1. Installiere phpMyAdmin:
    ```bash
    sudo apt install phpmyadmin
    ```
2. Wähle während der Installation den Webserver aus (z.B. Apache2) und konfiguriere die Datenbank für phpMyAdmin.

## Schritt 3: MariaDB konfigurieren

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

## Schritt 4: MariaDB für Fernzugriff konfigurieren

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

## Schritt 5: Firewall konfigurieren

1. Erlaube den Fernzugriff auf den MariaDB-Port (3306):
    ```bash
    sudo ufw allow 3306/tcp
    ```

## Schritt 6: phpMyAdmin konfigurieren

1. Öffne deinen Webbrowser und navigiere zu `http://localhost/phpmyadmin`.
2. Melde dich mit dem neu erstellten Benutzer `benutzer` und dem Passwort `passwort` an.
3. Wähle die Datenbank `WerteDB` aus und erstelle die Tabelle `messung`:
    ```sql
    CREATE TABLE messung (
        id INT AUTO_INCREMENT PRIMARY KEY,
        datum DATETIME,
        sensorName VARCHAR(50),
        Wert FLOAT
    );
    ```

## Schritt 7: Datenbank in phpMyAdmin erstellen

1. Melde dich bei phpMyAdmin an, indem du `http://localhost/phpmyadmin` in deinem Webbrowser aufrufst.
2. Gib den Benutzernamen `root` und das Passwort ein, das du während der MariaDB-Installation festgelegt hast.
3. Klicke auf "Datenbanken" im oberen Menü.
4. Gib unter "Datenbank erstellen" den Namen `WerteDB` ein und klicke auf "Anlegen".
5. Wähle die neu erstellte Datenbank `WerteDB` aus der Liste auf der linken Seite aus.
6. Klicke auf "SQL" im oberen Menü und füge das folgende SQL-Skript ein, um die Tabelle `messung` zu erstellen:
    ```sql
    CREATE TABLE messung (
        id INT AUTO_INCREMENT PRIMARY KEY,
        datum DATETIME,
        sensorName VARCHAR(50),
        Wert FLOAT
    );
    ```
7. Klicke auf "OK", um das Skript auszuführen und die Tabelle zu erstellen.

## Fertig!

Du hast nun MariaDB und phpMyAdmin installiert und eine Datenbank eingerichtet. Du kannst nun Sensordaten in die Datenbank speichern und verwalten und von anderen Geräten aus darauf zugreifen. Ändere die main.py so um, das es sich mit ihrer Datenbank verbindet und die Sensordaten speichert.
