### Datenübertragung

Dieses Projekt wird sich darauf beziehen, Sensorenübertragung durchzuführen. Auch wird sich mit den Auswerten eines Strings bschäftigt


## Der Plan (Protokoll zur Sensordatenübertragung)

:T00+000.1;      wobei

: = Startzeichen
T = Art des Sensores
00 = Nummern des Sensors
+ = Vorzeichen
000.0 = Stellenanzahl 
; = Abschlusszeichen

Das Programm soll mithilfe eines Übergabeparameters gestartet werden
Beispiel: python main.py ":T01+015.1;"

Der Code soll dann zuerst folgendes Ausgeben:
1. Hallo:_ :T01+015.1;
2. :
3. T
4. 01
5. +
6. 015.1
7. ;
8. date
9. date als Zahl
