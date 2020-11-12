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

## Aufbau
### main.py
In main.py wird das Modell durchlaufen sowie die Daten gesammelt und visualisiert.
### /models
 Models befinden sich in /models.
 In einem Model (Umgebung) werden die Parameter der Simulation gesetzt und die Agenten hinzugefügt. 
 Die Daten zur Analyse werden hier generiert.
 
### agents.py
In agents.py werden die einzelnen Agenten definiert.
- Person(): "Normalo", Grundgerüst für alle Unterklassen. Implementiert lifecycle().
- Devil(): Eine durchweg egostisch handelnde Person
- Angel(): Eine durchweg altruistisch handelnde Person