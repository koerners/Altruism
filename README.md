# Agent based Altruism Simulation

## Installation
Requirements installieren
```
pip install -r requirements.txt
```

Simulation starten
```
python3 main.py
```
Die Ergebnisse befinden sich in /out/


## Visualisierung
Eine Live Visualisierung befindet sich in der Testphase.
Getestet werden kann diese mit
````
python3 server.py
````
Wenn man nun auf die angezeigte URL (meist http://127.0.0.1:5000/) wechselt, kann der Verlauf live verfolgt werden.


## Aufbau
### main.py
In main.py wird das Modell durchlaufen sowie die Daten gesammelt und visualisiert.
In der Klasse Parameters können die Simualtionsparameter gesetzt werden.
### /models
 Models befinden sich in /models.
 In einem Model (Umgebung) werden die Parameter der Simulation gesetzt und die Agenten hinzugefügt. 
 Die Daten zur Analyse werden hier generiert.
 
### agents.py
In agents.py werden die einzelnen Agenten definiert.
- Person(): "Normalo", Grundgerüst für alle Unterklassen. Implementiert lifecycle().
- Devil(): Eine durchweg egostisch handelnde Person
- Angel(): Eine durchweg altruistisch handelnde Person