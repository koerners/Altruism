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

## run_sim-Funktion

Die Smulation wird mit der folgenden Funktion gestartet mit den Parametern:

- id_: Name des Ordners in dem der Output gespeichert wird bzw. bei Batch-Durchläufen die ID der Parameterkombination in
  der Tabelle
- param: Die parameter der Klasse *Parameter*
- no_img (optional): Wenn *True* werden keine Graphen generiert (nützlich bei Batch)

````
run_sim(id_, param, no_img=False)
````

## Batch-Durchläufe

Sollen mehrere Parameter getestet werden, kann in der main.py die Variable  ``BATCH`` auf *True* gesetzt werden, wodurch
die Parameter aus ``batch_parameter.csv`` eingelesen werden.

## Aufbau

### main.py

In main.py wird das Modell durchlaufen sowie die Daten gesammelt und visualisiert. In der Klasse Parameters können die
Simualtionsparameter gesetzt werden.

### /models

Models befinden sich in /models. In einem Model (Umgebung) werden die Parameter der Simulation gesetzt und die Agenten
hinzugefügt. Die Daten zur Analyse werden hier generiert.
 
### agents.py
In agents.py werden die einzelnen Agenten definiert.
- BaseAgent(): "Normalo", Grundgerüst für alle Unterklassen. Implementiert lifecycle().
- NonAltruist(): Eine durchweg egostisch handelnde BaseAgent
- Altruist(): Eine durchweg altruistisch handelnde BaseAgent