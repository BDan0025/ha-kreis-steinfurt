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
- `sensor.kreis_steinfurt_einsatzhistorie` – Anzahl der gespeicherten Einsätze
  innerhalb der gewählten Aufbewahrungsdauer
- `sensor.kreis_steinfurt_einsaetze_heute` – Gesamtzahl seit Tagesbeginn
- `sensor.kreis_steinfurt_einsaetze_letzte_7_tage` – Gesamtzahl der letzten
  sieben Tage
- `sensor.kreis_steinfurt_einsatzarten` – bekannte Einsatzarten mit Zählern in
  den Attributen

Zusätzlich entstehen dynamisch Sensoren für jeden Einsatz sowie jede in der
Liste vorkommende Stadt. Ein Einsatzsensor hat den Status als Zustand und die
Attribute `einsatznummer`, `einsatzart`, `ort`, `beginn`, `status`, `strasse`,
`sachverhalt`, `latitude` und `longitude`. Straße, Sachverhalt und Koordinaten
sind `null`, solange die öffentliche Quelle diese Angaben nicht veröffentlicht.
Zusätzlich sind `erstmals_gesehen`, `letzte_aenderung`, `abgeschlossen_am`,
`dauer_sekunden` und `dauer` vorhanden. Die dynamische Entity wird nach Ablauf
der ausgewählten Aufbewahrung entfernt; die Einsatzhistorie enthält den
kompletten Verlauf bis zu diesem Zeitpunkt.

## Dashboard-Beispiel

Eine fertige Lovelace-Vorlage mit Übersicht und einer Einsatzliste für
Ibbenbüren liegt in [`examples/lovelace_cards.yaml`](examples/lovelace_cards.yaml).
Den YAML-Inhalt als **Manuelle Karte** in einem Home-Assistant-Dashboard
einfügen. Für eine andere Stadt in der Markdown-Karte sowohl den Titel als auch
die Entity-ID `sensor.kreis_steinfurt_einsaetze_ibbenbueren` anpassen.

Die Karte [`examples/lovelace_last_incident_card.yaml`](examples/lovelace_last_incident_card.yaml)
zeigt den neuesten Einsatz mit Beginn, bisheriger Dauer sowie Zählern für aktive
und abgeschlossene Einsätze im ausgewählten Überwachungsgebiet.

[`examples/lovelace_incident_lists.yaml`](examples/lovelace_incident_lists.yaml)
enthält eine fertige Karte mit Statistik, einer Liste laufender Einsätze und
einer Historienliste.

Die Angaben stammen ausschließlich von der veröffentlichten Liste des Kreises
Steinfurt und können sich jederzeit ändern.

## Versionierung

Diese Integration verwendet das Schema `X.Y.Z`:

| Stelle | Bedeutung | Erhöhung bei |
| --- | --- | --- |
| `X` | Hauptversion | grundlegenden Umbauten oder Architekturänderungen |
| `Y` | Funktionsversion | neuen Funktionen, Entitäten oder Berechnungen |
| `Z` | Korrekturversion | Fehlerbehebungen und Verbesserungen ohne neue Funktion |

Eine neue Version muss zunächst erfolgreich in Home Assistant eingerichtet und
gelaufen sein. Fehler, die beim erstmaligen Einrichten einer neuen Version
auftreten, werden noch unter derselben Versionsnummer korrigiert. Erst danach
wird für eine nachträgliche reine Fehlerkorrektur `Z` erhöht. Bei einer neuen
Funktionsversion wird `Z` wieder auf `0` gesetzt.

Der vorbereitete Stand mit Einstellungsseite, Gebietsfilter und
Aufbewahrungszeit, Historie und Statistik ist **0.2.0**. Er muss erst
erfolgreich laufen, bevor eine Korrekturversion wie `0.2.1` vergeben wird.

## Einstellungen

Unter **Einstellungen → Geräte & Dienste → Kreis Steinfurt Einsätze →
Konfigurieren** lassen sich die überwachten Kommunen per Mehrfachauswahl festlegen.
Die Übersichtssensoren sowie Einsatz- und Ortssensoren berücksichtigen nur diese
Auswahl.

Die Einsatzarten werden aus den veröffentlichten Daten automatisch erkannt und
lassen sich dort ebenfalls per Mehrfachauswahl ein- oder ausschalten. Eine neue
Einsatzart erscheint nach dem ersten Abruf in dieser Auswahl.

Für einzelne Einsatz-Entities kann eine Aufbewahrung von 48 Stunden, 7 Tagen,
einem Monat oder dauerhaft gewählt werden. Die Integration speichert dafür die
zuletzt veröffentlichten Einsatzdetails lokal in Home Assistant und entfernt die
Entity nach Ablauf der gewählten Zeit.

Die Sensoren „heute“ und „letzte 7 Tage“ verwenden diese gespeicherte Historie.
Für eine vollständige 7-Tage-Statistik muss die Aufbewahrung deshalb mindestens
auf 7 Tage, 1 Monat oder „Nie“ eingestellt sein.

## Entwicklung

```shell
python -m pip install -r requirements_dev.txt
python -m pytest
```
