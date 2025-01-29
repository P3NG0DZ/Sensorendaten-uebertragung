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

Es wurde extra ein MariaDB-Server aufgesetzt, um die Sensordaten in einer Datenbank zu speichern. Genutz wurde hier eine Raspberry Pi 3b+.
Bis jetzt wird sie auch noch lokal gepseichert.

Zudem soll es auch möglich sein, dass es einen komplexen Eingabestring verarbeiten kann.

Beispiel: `:T00+001.0T01+002.0T02+003.0T03+010.0T04+011.0T05+012.0T06+010.0T07+011.0T08+012.0;`
Der Eingabestring erhält mehrere Sensordaten, die nacheinandern verarbeitet werden sollen.

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
4. Gibt das aktuelle Datum und das Datum als Long-Wert und umgewandeltes Datum zurück.
5. Speichert die Sensordaten in einer lokalen Datenbank. (Bis jetzt, später mit Datenbankserver)


