### Datenübertragung

Dieses Projekt wird sich darauf beziehen, Sensorenübertragung durchzuführen. Auch wird sich mit dem Auswerten eines Strings beschäftigt.

Es handelt sich hierbei um ein Schulprojekt. Nichts spannendes. Die Repo  ist wegen Klassenkameraden aktiv, damit die sich hilfe holen können falls ich nicht da bin oder nicht weiterkommen! Wer gerne meinen Weg verfolgen will oder so ein ähnliches Projekt hat, fühlt euch frei, diesen Code etwas zu verändern oder zu nutzen :)

Diese Werte werden dann in einer Datenbank angelegt (Bis jetzt lokal).
Ziel ist es aber dann mit einem Datenbankserver.

## Der Plan (Protokoll zur Sensordatenübertragung)

:T00+000.1;      wobei

: = Startzeichen  
T = Art des Sensors  
00 = Nummer des Sensors  
+ = Vorzeichen  
000.0 = Stellenanzahl  
; = Abschlusszeichen  

Das Programm soll mithilfe eines Übergabeparameters gestartet werden.  
Beispiel: `python main.py ":T01+015.1;"`

Der Code soll dann zuerst folgendes ausgeben:
1. Hallo:_ :T01+015.1;
2. :
3. T
4. 01
5. +
6. 015.1
7. ;
8. Datum
9. Datum als Zahl

## Erklärung des Python Codes:

### parse_sensor_data(data)
Diese Funktion nimmt einen String `data` im Sensordatenformat und zerlegt ihn in seine Bestandteile:
- `start`: Startzeichen
- `sensor_type`: Art des Sensors
- `sensor_number`: Nummer des Sensors
- `sign`: Vorzeichen
- `value`: Wert des Sensors
- `end`: Abschlusszeichen

### Hauptprogramm
Das Hauptprogramm führt folgende Schritte aus:
1. Überprüft, ob das Programm mit genau einem Parameter gestartet wurde.
2. Gibt den übergebenen Sensordaten-String aus.
3. Zerlegt den Sensordaten-String in seine Bestandteile und gibt diese aus.
4. Gibt das aktuelle Datum und das Datum im Format JJJJMMTT aus.
