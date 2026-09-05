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

Die Integration erstellt diese Übersichten:

- `sensor.kreis_steinfurt_einsaetze` – Anzahl aller veröffentlichten Einsätze
  der letzten 48 Stunden
- `sensor.kreis_steinfurt_laufende_einsaetze` – Anzahl der Einträge, die nicht
  als `abgeschlossen` markiert sind
- `sensor.kreis_steinfurt_einsaetze_letzte_24_stunden` – Anzahl seit den
  vergangenen 24 Stunden

Zusätzlich entstehen dynamisch Sensoren für jeden Einsatz sowie jede in der
Liste vorkommende Stadt. Ein Einsatzsensor hat den Status als Zustand und die
Attribute `einsatznummer`, `einsatzart`, `ort`, `beginn`, `status`, `strasse`,
`sachverhalt`, `latitude` und `longitude`. Straße, Sachverhalt und Koordinaten
sind `null`, solange die öffentliche Quelle diese Angaben nicht veröffentlicht.
Ein Einsatzsensor wird nicht gelöscht, sondern nach Ablauf der 48 Stunden als
`unavailable` markiert. Damit bleibt sein Verlauf in Home Assistant erhalten.

Die Angaben stammen ausschließlich von der veröffentlichten Liste des Kreises
Steinfurt und können sich jederzeit ändern.

## Entwicklung

```shell
python -m pip install -r requirements_dev.txt
python -m pytest
```
