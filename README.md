# Kreis Steinfurt Einsätze für Home Assistant

Diese Custom Integration liest die öffentlich verfügbare Liste der
[aktuellen Einsätze](https://www.kreis-steinfurt.de/kv_steinfurt/Kreisverwaltung/%C3%84mter/Amt%20f%C3%BCr%20Bev%C3%B6lkerungsschutz/Kreisleitstelle/Aktuelle%20Eins%C3%A4tze/)
der Feuerwehren im Kreis Steinfurt aus.

Die Quelle enthält Einsätze der letzten 48 Stunden. Sie wird standardmäßig alle
60 Sekunden aktualisiert.

## Installation

1. Den Ordner `custom_components/kreis_steinfurt` nach
   `<Home-Assistant-Konfiguration>/custom_components/kreis_steinfurt` kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach
   **Kreis Steinfurt Einsätze** suchen und einrichten.

## Sensor

Die Integration erstellt `sensor.kreis_steinfurt_einsaetze_…`. Sein Zustand ist
die Anzahl aller von der Quelle gelisteten Einsätze. Die Attribute enthalten:

- `einsatzanzahl_letzte_48_stunden`
- `laufende_einsaetze` – Zahl aller Einträge, deren Zustand nicht
  `abgeschlossen` ist
- `einsatznummern` und `orte`
- `einsaetze` – Liste mit Einsatznummer, Einsatzart, Ort, Beginn und Zustand

Die Angaben stammen ausschließlich von der veröffentlichten Liste des Kreises
Steinfurt und können sich jederzeit ändern.

## Entwicklung

```shell
python -m pip install -r requirements_dev.txt
python -m pytest
```
